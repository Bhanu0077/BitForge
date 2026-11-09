package server;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.OutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.sql.*;
import java.util.HashMap;
import java.util.Map;

public class BitForgeServer {
    private static final int PORT = 8080;
    private static final String DB_URL = "jdbc:sqlite:database/bitforge.db";

    public static void main(String[] args) throws Exception {
        try {
            Class.forName("org.sqlite.JDBC");
        } catch (ClassNotFoundException e) {
            System.out.println("SQLite JDBC Driver check.");
        }

        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        server.createContext("/api/signup", new SignupHandler());
        server.createContext("/api/login", new LoginHandler());
        server.createContext("/api/forgot-password", new ForgotPasswordHandler());
        server.createContext("/api/sync", new SyncHandler());
        server.createContext("/api/transaction", new TransactionHandler());
        server.createContext("/api/mine", new MiningHandler());

        server.setExecutor(null);
        System.out.println("BitForge Java Server running on port " + PORT);
        server.start();
    }

    private static Map<String, String> parseBody(InputStream is) throws IOException {
        String body = new String(is.readAllBytes(), StandardCharsets.UTF_8);
        Map<String, String> params = new HashMap<>();
        if (body.isEmpty()) return params;
        
        for (String pair : body.split("&")) {
            String[] kv = pair.split("=");
            if (kv.length == 2) {
                params.put(java.net.URLDecoder.decode(kv[0], StandardCharsets.UTF_8),
                           java.net.URLDecoder.decode(kv[1], StandardCharsets.UTF_8));
            } else if (kv.length == 1) {
                params.put(java.net.URLDecoder.decode(kv[0], StandardCharsets.UTF_8), "");
            }
        }
        return params;
    }

    private static void sendResponse(HttpExchange exchange, int code, String response) throws IOException {
        exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type");
        exchange.getResponseHeaders().add("Content-Type", "application/json");

        if (exchange.getRequestMethod().equalsIgnoreCase("OPTIONS")) {
            exchange.sendResponseHeaders(204, -1);
            return;
        }

        byte[] bytes = response.getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(code, bytes.length);
        OutputStream os = exchange.getResponseBody();
        os.write(bytes);
        os.close();
    }

    private static String hashPassword(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(password.getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            return password;
        }
    }

    static class SignupHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) { sendResponse(exchange, 200, ""); return; }
            Map<String, String> params = parseBody(exchange.getRequestBody());
            String email = params.get("email");
            String password = params.get("password");
            String question = params.get("question");
            String answer = params.get("answer");

            if (email == null || password == null || question == null || answer == null) {
                sendResponse(exchange, 400, "{\"success\": false, \"message\": \"All fields are required.\"}");
                return;
            }

            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                String sql = "INSERT INTO users (email, password_hash, secret_question, secret_answer, balance) VALUES (?, ?, ?, ?, 100.0)";
                PreparedStatement stmt = conn.prepareStatement(sql);
                stmt.setString(1, email);
                stmt.setString(2, hashPassword(password));
                stmt.setString(3, question);
                stmt.setString(4, answer.toLowerCase().trim());
                stmt.executeUpdate();

                sendResponse(exchange, 200, "{\"success\": true, \"message\": \"Signup successful! User added to ecosystem.\"}");
            } catch (SQLException e) {
                sendResponse(exchange, 400, "{\"success\": false, \"message\": \"User already exists or database error.\"}");
            }
        }
    }

    static class LoginHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) { sendResponse(exchange, 200, ""); return; }
            Map<String, String> params = parseBody(exchange.getRequestBody());
            String email = params.get("email");
            String password = params.get("password");

            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                String sql = "SELECT email, balance FROM users WHERE email = ? AND password_hash = ?";
                PreparedStatement stmt = conn.prepareStatement(sql);
                stmt.setString(1, email);
                stmt.setString(2, hashPassword(password));
                ResultSet rs = stmt.executeQuery();

                if (rs.next()) {
                    double balance = rs.getDouble("balance");
                    sendResponse(exchange, 200, String.format("{\"success\": true, \"email\": \"%s\", \"balance\": %.2f}", email, balance));
                } else {
                    sendResponse(exchange, 401, "{\"success\": false, \"message\": \"Invalid email or password.\"}");
                }
            } catch (SQLException e) {
                sendResponse(exchange, 500, "{\"success\": false, \"message\": \"Database error.\"}");
            }
        }
    }

    static class ForgotPasswordHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) { sendResponse(exchange, 200, ""); return; }
            Map<String, String> params = parseBody(exchange.getRequestBody());
            String email = params.get("email");
            String answer = params.get("answer");
            String newPassword = params.get("new_password");

            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                String sql = "SELECT secret_answer FROM users WHERE email = ?";
                PreparedStatement stmt = conn.prepareStatement(sql);
                stmt.setString(1, email);
                ResultSet rs = stmt.executeQuery();

                if (rs.next()) {
                    String storedAnswer = rs.getString("secret_answer");
                    if (storedAnswer.equalsIgnoreCase(answer.trim())) {
                        String updateSql = "UPDATE users SET password_hash = ? WHERE email = ?";
                        PreparedStatement updateStmt = conn.prepareStatement(updateSql);
                        updateStmt.setString(1, hashPassword(newPassword));
                        updateStmt.setString(2, email);
                        updateStmt.executeUpdate();

                        sendResponse(exchange, 200, "{\"success\": true, \"message\": \"Password updated successfully!\"}");
                        return;
                    }
                }
                sendResponse(exchange, 400, "{\"success\": false, \"message\": \"Verification failed. Incorrect answer.\"}");
            } catch (SQLException e) {
                sendResponse(exchange, 500, "{\"success\": false, \"message\": \"Database error.\"}");
            }
        }
    }

    static class SyncHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) { sendResponse(exchange, 200, ""); return; }
            
            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                Statement stmt = conn.createStatement();
                ResultSet rsTxs = stmt.executeQuery("SELECT * FROM transactions ORDER BY id DESC LIMIT 50");
                StringBuilder txsJson = new StringBuilder("[");
                while (rsTxs.next()) {
                    txsJson.append(String.format("{\"from\":\"%s\",\"to\":\"%s\",\"amount\":%.2f,\"time\":\"%s\",\"status\":\"%s\"},",
                        rsTxs.getString("sender_email"), rsTxs.getString("receiver_email"),
                        rsTxs.getDouble("amount"), rsTxs.getString("timestamp"), rsTxs.getString("status")));
                }
                if (txsJson.length() > 1) txsJson.deleteCharAt(txsJson.length() - 1);
                txsJson.append("]");

                ResultSet rsBlocks = stmt.executeQuery("SELECT * FROM blockchain ORDER BY block_index DESC");
                StringBuilder blocksJson = new StringBuilder("[");
                while (rsBlocks.next()) {
                    blocksJson.append(String.format("{\"index\":%d,\"hash\":\"%s\",\"prev\":\"%s\",\"data\":\"%s\",\"time\":\"%s\"},",
                        rsBlocks.getInt("block_index"), rsBlocks.getString("current_hash"),
                        rsBlocks.getString("previous_hash"), rsBlocks.getString("transactions_data"),
                        rsBlocks.getString("timestamp")));
                }
                if (blocksJson.length() > 1) blocksJson.deleteCharAt(blocksJson.length() - 1);
                blocksJson.append("]");

                String json = String.format("{\"transactions\": %s, \"blocks\": %s}", txsJson.toString(), blocksJson.toString());
                sendResponse(exchange, 200, json);
            } catch (SQLException e) {
                sendResponse(exchange, 500, "{\"success\": false, \"message\": \"Database sync failed.\"}");
            }
        }
    }

    static class TransactionHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) { sendResponse(exchange, 200, ""); return; }
            Map<String, String> params = parseBody(exchange.getRequestBody());
            String sender = params.get("sender");
            String receiver = params.get("receiver");
            double amount;

            try {
                amount = Double.parseDouble(params.get("amount"));
            } catch (Exception e) {
                sendResponse(exchange, 400, "{\"success\": false, \"message\": \"Invalid amount.\"}");
                return;
            }

            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                conn.setAutoCommit(false);

                PreparedStatement checkSender = conn.prepareStatement("SELECT balance FROM users WHERE email = ?");
                checkSender.setString(1, sender);
                ResultSet rs = checkSender.executeQuery();
                if (!rs.next() || rs.getDouble("balance") < amount) {
                    conn.rollback();
                    sendResponse(exchange, 400, "{\"success\": false, \"message\": \"Insufficient balance or invalid sender.\"}");
                    return;
                }

                PreparedStatement checkReceiver = conn.prepareStatement("SELECT balance FROM users WHERE email = ?");
                checkReceiver.setString(1, receiver);
                if (!checkReceiver.executeQuery().next()) {
                    conn.rollback();
                    sendResponse(exchange, 400, "{\"success\": false, \"message\": \"Receiver account does not exist.\"}");
                    return;
                }

                PreparedStatement deduct = conn.prepareStatement("UPDATE users SET balance = balance - ? WHERE email = ?");
                deduct.setDouble(1, amount);
                deduct.setString(2, sender);
                deduct.executeUpdate();

                PreparedStatement credit = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE email = ?");
                credit.setDouble(1, amount);
                credit.setString(2, receiver);
                credit.executeUpdate();

                PreparedStatement logTx = conn.prepareStatement("INSERT INTO transactions (sender_email, receiver_email, amount, timestamp, status) VALUES (?, ?, ?, DATETIME('now'), 'unconfirmed')");
                logTx.setString(1, sender);
                logTx.setString(2, receiver);
                logTx.setDouble(3, amount);
                logTx.executeUpdate();

                conn.commit();
                sendResponse(exchange, 200, "{\"success\": true, \"message\": \"Transaction executed successfully!\"}");
            } catch (SQLException e) {
                sendResponse(exchange, 500, "{\"success\": false, \"message\": \"Transaction failed.\"}");
            }
        }
    }

    static class MiningHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) { sendResponse(exchange, 200, ""); return; }
            Map<String, String> params = parseBody(exchange.getRequestBody());
            String miner = params.get("miner");

            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                Statement stmt = conn.createStatement();
                ResultSet rsLast = stmt.executeQuery("SELECT block_index, current_hash FROM blockchain ORDER BY block_index DESC LIMIT 1");
                
                int nextIndex = 1;
                String prevHash = "0000000000000000000000000000000000000000000000000000000000000000";
                if (rsLast.next()) {
                    nextIndex = rsLast.getInt("block_index") + 1;
                    prevHash = rsLast.getString("current_hash");
                }

                String currentHash = hashPassword("block_" + nextIndex + "_" + System.currentTimeMillis());
                
                PreparedStatement addBlock = conn.prepareStatement("INSERT INTO blockchain (block_index, previous_hash, current_hash, nonce, timestamp, transactions_data) VALUES (?, ?, ?, ?, DATETIME('now'), ?)");
                addBlock.setInt(1, nextIndex);
                addBlock.setString(2, prevHash);
                addBlock.setString(3, currentHash);
                addBlock.setInt(4, (int)(Math.random() * 100000));
                addBlock.setString(5, "Mined by " + (miner != null ? miner : "Network Miner"));
                addBlock.executeUpdate();

                if (miner != null) {
                    PreparedStatement reward = conn.prepareStatement("UPDATE users SET balance = balance + 10 WHERE email = ?");
                    reward.setString(1, miner);
                    reward.executeUpdate();
                }

                sendResponse(exchange, 200, String.format("{\"success\": true, \"block\": %d, \"hash\": \"%s\", \"message\": \"Block #%d mined! 10 BFG reward credited.\"}", nextIndex, currentHash, nextIndex));
            } catch (SQLException e) {
                sendResponse(exchange, 500, "{\"success\": false, \"message\": \"Mining failed.\"}");
            }
        }
    }
}
