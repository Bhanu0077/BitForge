# 1. AuthServlet.java
auth_code = '''package com.bitforge;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

@WebServlet("/api/auth/*")
public class AuthServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String path = req.getPathInfo();

        if ("/signup".equals(path)) {
            String username = req.getParameter("username");
            String password = req.getParameter("password");
            String question = req.getParameter("question");
            String answer = req.getParameter("answer");

            if (username == null || password == null) {
                out.print("{\\"success\\": false, \\"message\\": \\"Username and password required\\"}");
                return;
            }

            try (Connection conn = DatabaseManager.getConnection()) {
                PreparedStatement pstmt = conn.prepareStatement(
                    "INSERT INTO users (username, password_hash, secret_question, secret_answer, balance) VALUES (?, ?, ?, ?, 100.0)"
                );
                pstmt.setString(1, username.trim().toLowerCase());
                pstmt.setString(2, password);
                pstmt.setString(3, question != null ? question : "default");
                pstmt.setString(4, answer != null ? answer : "default");
                pstmt.executeUpdate();

                out.print(String.format("{\\"success\\": true, \\"message\\": \\"Account created successfully\\", \\"username\\": \\"%s\\"}", username.trim().toLowerCase()));
            } catch (Exception e) {
                out.print("{\\"success\\": false, \\"message\\": \\"Username already exists!\\"}");
            }

        } else if ("/login".equals(path)) {
            String username = req.getParameter("username");
            String password = req.getParameter("password");

            try (Connection conn = DatabaseManager.getConnection()) {
                PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND password_hash = ?");
                pstmt.setString(1, username != null ? username.trim() : "");
                pstmt.setString(2, password);
                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    out.print(String.format("{\\"success\\": true, \\"username\\": \\"%s\\"}", rs.getString("username")));
                } else {
                    out.print("{\\"success\\": false, \\"message\\": \\"Invalid username or password\\"}");
                }
            } catch (Exception e) {
                out.print("{\\"success\\": false, \\"message\\": \\"Database error\\"}");
            }

        } else if ("/forgot-password".equals(path)) {
            String username = req.getParameter("username");
            String answer = req.getParameter("answer");
            String newPassword = req.getParameter("new_password");

            try (Connection conn = DatabaseManager.getConnection()) {
                PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND LOWER(secret_answer) = LOWER(?)");
                pstmt.setString(1, username != null ? username.trim() : "");
                pstmt.setString(2, answer != null ? answer.trim() : "");
                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    PreparedStatement updatePstmt = conn.prepareStatement("UPDATE users SET password_hash = ? WHERE LOWER(username) = LOWER(?)");
                    updatePstmt.setString(1, newPassword);
                    updatePstmt.setString(2, username.trim());
                    updatePstmt.executeUpdate();

                    out.print("{\\"success\\": true, \\"message\\": \\"Password updated successfully!\\"}");
                } else {
                    out.print("{\\"success\\": false, \\"message\\": \\"Incorrect secret answer or username\\"}");
                }
            } catch (Exception e) {
                out.print("{\\"success\\": false, \\"message\\": \\"Recovery error\\"}");
            }
        }
    }
}
'''

# 2. UserServlet.java
user_code = '''package com.bitforge;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

@WebServlet("/api/user/*")
public class UserServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String username = req.getParameter("username");

        if (username == null || username.trim().isEmpty()) {
            out.print("{\\"success\\": false, \\"message\\": \\"Username required\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            PreparedStatement pstmt = conn.prepareStatement("SELECT balance, is_private FROM users WHERE LOWER(username) = LOWER(?)");
            pstmt.setString(1, username.trim());
            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                double balance = rs.getDouble("balance");
                boolean isPrivate = rs.getInt("is_private") == 1;
                out.print(String.format("{\\"success\\": true, \\"balance\\": %.2f, \\"is_private\\": %b}", balance, isPrivate));
            } else {
                out.print("{\\"success\\": false, \\"message\\": \\"User not found\\"}");
            }
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"DB error\\"}");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String username = req.getParameter("username");
        String toggle = req.getParameter("toggle");

        if (username == null || toggle == null) {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid params\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            PreparedStatement pstmt = conn.prepareStatement("UPDATE users SET is_private = ? WHERE LOWER(username) = LOWER(?)");
            pstmt.setInt(1, "true".equalsIgnoreCase(toggle) ? 1 : 0);
            pstmt.setString(2, username.trim());
            pstmt.executeUpdate();

            out.print("{\\"success\\": true}");
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"DB update error\\"}");
        }
    }
}
'''

# 3. TransactionServlet.java
tx_code = '''package com.bitforge;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

@WebServlet("/api/transactions/*")
public class TransactionServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        StringBuilder txsJson = new StringBuilder("[");
        StringBuilder usersJson = new StringBuilder("[");

        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            ResultSet rsTxs = stmt.executeQuery("SELECT sender_username, receiver_username, amount, timestamp FROM transactions ORDER BY id DESC");
            while (rsTxs.next()) {
                txsJson.append(String.format("{\\"from\\":\\"%s\\",\\"to\\":\\"%s\\",\\"amount\\":%.2f,\\"time\\":\\"%s\\"},",
                        rsTxs.getString("sender_username"), rsTxs.getString("receiver_username"),
                        rsTxs.getDouble("amount"), rsTxs.getTimestamp("timestamp").toString()));
            }
            if (txsJson.length() > 1) txsJson.deleteCharAt(txsJson.length() - 1);

            ResultSet rsUsers = stmt.executeQuery("SELECT username FROM users");
            while (rsUsers.next()) {
                usersJson.append(String.format("{\\"username\\":\\"%s\\"},", rsUsers.getString("username")));
            }
            if (usersJson.length() > 1) usersJson.deleteCharAt(usersJson.length() - 1);

        } catch (Exception ignored) {}

        txsJson.append("]");
        usersJson.append("]");

        out.print(String.format("{\\"success\\": true, \\"transactions\\": %s, \\"users\\": %s}", txsJson.toString(), usersJson.toString()));
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        String sender = req.getParameter("sender");
        String receiver = req.getParameter("receiver");
        double amount = 0;

        try {
            amount = Double.parseDouble(req.getParameter("amount"));
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid amount\\"}");
            return;
        }

        if (sender == null || receiver == null || amount <= 0) {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid parameters\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            conn.setAutoCommit(false);

            PreparedStatement checkBal = conn.prepareStatement("SELECT balance FROM users WHERE LOWER(username) = LOWER(?)");
            checkBal.setString(1, sender.trim());
            ResultSet rs = checkBal.executeQuery();

            if (!rs.next() || rs.getDouble("balance") < amount) {
                conn.rollback();
                out.print("{\\"success\\": false, \\"message\\": \\"Insufficient account balance!\\"}");
                return;
            }

            PreparedStatement checkRec = conn.prepareStatement("SELECT balance FROM users WHERE LOWER(username) = LOWER(?)");
            checkRec.setString(1, receiver.trim());
            if (!checkRec.executeQuery().next()) {
                conn.rollback();
                out.print("{\\"success\\": false, \\"message\\": \\"Receiver username not found!\\"}");
                return;
            }

            PreparedStatement deduct = conn.prepareStatement("UPDATE users SET balance = balance - ? WHERE LOWER(username) = LOWER(?)");
            deduct.setDouble(1, amount);
            deduct.setString(2, sender.trim());
            deduct.executeUpdate();

            PreparedStatement add = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE LOWER(username) = LOWER(?)");
            add.setDouble(1, amount);
            add.setString(2, receiver.trim());
            add.executeUpdate();

            PreparedStatement logTx = conn.prepareStatement("INSERT INTO transactions (sender_username, receiver_username, amount) VALUES (?, ?, ?)");
            logTx.setString(1, sender.trim());
            logTx.setString(2, receiver.trim());
            logTx.setDouble(3, amount);
            logTx.executeUpdate();

            conn.commit();
            out.print("{\\"success\\": true, \\"message\\": \\"Transfer successful!\\"}");

        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Transaction error\\"}");
        }
    }
}
'''

# 4. NetworkServlet.java
network_code = '''package com.bitforge;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

@WebServlet("/api/network/*")
public class NetworkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        StringBuilder peersJson = new StringBuilder("[");
        int userCount = 0;
        int txCount = 0;
        int blockCount = 0;

        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            ResultSet rsUsers = stmt.executeQuery("SELECT username, balance, is_private FROM users ORDER BY id DESC");
            while (rsUsers.next()) {
                userCount++;
                boolean isPrivate = rsUsers.getInt("is_private") == 1;
                double balance = rsUsers.getDouble("balance");

                peersJson.append(String.format("{\\"username\\":\\"%s\\",\\"balance\\":%.2f,\\"is_private\\":%b},",
                    rsUsers.getString("username"), balance, isPrivate));
            }
            if (peersJson.length() > 1) peersJson.deleteCharAt(peersJson.length() - 1);

            ResultSet rsTxs = stmt.executeQuery("SELECT COUNT(*) FROM transactions");
            if (rsTxs.next()) txCount = rsTxs.getInt(1);

            ResultSet rsBlocks = stmt.executeQuery("SELECT COUNT(*) FROM blockchain");
            if (rsBlocks.next()) blockCount = rsBlocks.getInt(1);
        } catch (Exception ignored) {}
        peersJson.append("]");

        int cores = Runtime.getRuntime().availableProcessors();
        long freeMemMB = Runtime.getRuntime().freeMemory() / (1024 * 1024);

        String json = String.format(
            "{\\"success\\": true, \\"users\\": %d, \\"transactions\\": %d, \\"blocks\\": %d, \\"cores\\": %d, \\"freeMemMB\\": %d, \\"javaVersion\\": \\"%s\\", \\"peers\\": %s}",
            userCount, txCount, blockCount, cores, freeMemMB, System.getProperty("java.version"), peersJson.toString()
        );

        out.print(json);
    }
}
'''

with open("src/com/bitforge/AuthServlet.java", "w") as f:
    f.write(auth_code)

with open("src/com/bitforge/UserServlet.java", "w") as f:
    f.write(user_code)

with open("src/com/bitforge/TransactionServlet.java", "w") as f:
    f.write(tx_code)

with open("src/com/bitforge/NetworkServlet.java", "w") as f:
    f.write(network_code)

print("All Java servlets updated to use username!")
