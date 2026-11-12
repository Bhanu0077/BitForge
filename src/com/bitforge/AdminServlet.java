package com.bitforge;

import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Locale;

/**
 * Administrative API. Only the explicitly supported tables and columns are
 * exposed; arbitrary SQL is intentionally not accepted by this endpoint.
 */
@WebServlet("/api/admin/*")
public class AdminServlet extends HttpServlet {
    private static final String ADMIN_SESSION_KEY = "bitforgeAdminAuthenticated";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        prepareJson(resp);
        PrintWriter out = resp.getWriter();
        if (!isAdmin(req)) {
            forbidden(out);
            return;
        }

        String path = req.getPathInfo();
        if ("/overview".equals(path)) {
            writeOverview(out);
        } else if ("/users".equals(path)) {
            writeUsers(out);
        } else if ("/transactions".equals(path)) {
            writeTransactions(out);
        } else if ("/blocks".equals(path)) {
            writeBlocks(out);
        } else {
            error(out, "Unknown admin endpoint.");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        prepareJson(resp);
        PrintWriter out = resp.getWriter();
        String path = req.getPathInfo();

        if ("/login".equals(path)) {
            login(req, out);
            return;
        }
        if ("/logout".equals(path)) {
            HttpSession session = req.getSession(false);
            if (session != null) session.invalidate();
            out.print("{\"success\":true}");
            return;
        }
        if (!isAdmin(req)) {
            forbidden(out);
            return;
        }

        if ("/users".equals(path)) {
            createUser(req, out);
        } else if ("/users/update".equals(path)) {
            updateUser(req, out);
        } else if ("/users/delete".equals(path)) {
            deleteUser(req, out);
        } else if ("/transactions/update".equals(path)) {
            updateTransaction(req, out);
        } else if ("/transactions/delete".equals(path)) {
            deleteTransaction(req, out);
        } else {
            error(out, "Unknown admin endpoint.");
        }
    }

    private void login(HttpServletRequest req, PrintWriter out) {
        String configuredUsername = configuredValue("bitforge.admin.username", "BITFORGE_ADMIN_USERNAME");
        String configuredPassword = configuredValue("bitforge.admin.password", "BITFORGE_ADMIN_PASSWORD");
        String username = safe(req.getParameter("username"));
        String password = req.getParameter("password");

        if (configuredUsername == null || configuredPassword == null) {
            error(out, "Admin access has not been configured on this server.");
        } else if (configuredUsername.equals(username) && configuredPassword.equals(password)) {
            HttpSession session = req.getSession(true);
            session.setAttribute(ADMIN_SESSION_KEY, Boolean.TRUE);
            session.setMaxInactiveInterval(30 * 60);
            out.print("{\"success\":true}");
        } else {
            error(out, "Invalid administrator credentials.");
        }
    }

    private void writeOverview(PrintWriter out) {
        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            int users = count(stmt, "SELECT COUNT(*) FROM users");
            int transactions = count(stmt, "SELECT COUNT(*) FROM transactions");
            int blocks = count(stmt, "SELECT COUNT(*) FROM blockchain");
            out.printf(Locale.US,
                    "{\"success\":true,\"users\":%d,\"transactions\":%d,\"blocks\":%d}", users, transactions, blocks);
        } catch (Exception e) {
            error(out, "Unable to read database overview.");
        }
    }

    private void writeUsers(PrintWriter out) {
        StringBuilder json = new StringBuilder("{\"success\":true,\"users\":[");
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                     "SELECT id, username, balance, is_private FROM users ORDER BY id DESC");
             ResultSet rs = stmt.executeQuery()) {
            boolean first = true;
            while (rs.next()) {
                if (!first) json.append(',');
                json.append(String.format(Locale.US,
                        "{\"id\":%d,\"username\":\"%s\",\"balance\":%.2f,\"is_private\":%s}",
                        rs.getInt("id"), escapeJson(rs.getString("username")),
                        rs.getDouble("balance"), rs.getInt("is_private") == 1));
                first = false;
            }
            json.append("]}");
            out.print(json);
        } catch (Exception e) {
            error(out, "Unable to read users.");
        }
    }

    private void writeTransactions(PrintWriter out) {
        StringBuilder json = new StringBuilder("{\"success\":true,\"transactions\":[");
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                     "SELECT id, sender_username, receiver_username, amount, timestamp " +
                             "FROM transactions ORDER BY id DESC");
             ResultSet rs = stmt.executeQuery()) {
            boolean first = true;
            while (rs.next()) {
                if (!first) json.append(',');
                json.append(String.format(Locale.US,
                        "{\"id\":%d,\"sender\":\"%s\",\"receiver\":\"%s\",\"amount\":%.2f,\"timestamp\":\"%s\"}",
                        rs.getInt("id"), escapeJson(rs.getString("sender_username")),
                        escapeJson(rs.getString("receiver_username")), rs.getDouble("amount"),
                        escapeJson(String.valueOf(rs.getTimestamp("timestamp")))));
                first = false;
            }
            json.append("]}");
            out.print(json);
        } catch (Exception e) {
            error(out, "Unable to read transactions.");
        }
    }

    private void writeBlocks(PrintWriter out) {
        StringBuilder json = new StringBuilder("{\"success\":true,\"blocks\":[");
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                     "SELECT block_index, previous_hash, current_hash, nonce, timestamp, transactions_data " +
                             "FROM blockchain ORDER BY block_index ASC");
             ResultSet rs = stmt.executeQuery()) {
            boolean first = true;
            while (rs.next()) {
                if (!first) json.append(',');
                json.append(String.format(Locale.US,
                        "{\"index\":%d,\"previousHash\":\"%s\",\"currentHash\":\"%s\",\"nonce\":%d," +
                                "\"timestamp\":\"%s\",\"data\":\"%s\"}",
                        rs.getInt("block_index"), escapeJson(rs.getString("previous_hash")),
                        escapeJson(rs.getString("current_hash")), rs.getInt("nonce"),
                        escapeJson(String.valueOf(rs.getTimestamp("timestamp"))),
                        escapeJson(rs.getString("transactions_data"))));
                first = false;
            }
            json.append("]}");
            out.print(json);
        } catch (Exception e) {
            error(out, "Unable to read blockchain records.");
        }
    }

    private void createUser(HttpServletRequest req, PrintWriter out) {
        String username = safe(req.getParameter("username")).toLowerCase(Locale.ROOT);
        String password = req.getParameter("password");
        Double balance = decimal(req.getParameter("balance"));
        if (!username.matches("[a-z0-9_.-]{3,64}") || password == null || password.length() < 6
                || balance == null || balance < 0) {
            error(out, "Username, password, or balance is invalid.");
            return;
        }
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                     "INSERT INTO users (username, password_hash, secret_question, secret_answer, balance) " +
                             "VALUES (?, ?, ?, ?, ?)")) {
            stmt.setString(1, username);
            stmt.setString(2, password);
            stmt.setString(3, "admin-created");
            stmt.setString(4, "not-applicable");
            stmt.setDouble(5, balance);
            stmt.executeUpdate();
            success(out, "User created.");
        } catch (Exception e) {
            error(out, "Could not create user. The username may already exist.");
        }
    }

    private void updateUser(HttpServletRequest req, PrintWriter out) {
        int id = integer(req.getParameter("id"));
        String username = safe(req.getParameter("username")).toLowerCase(Locale.ROOT);
        Double balance = decimal(req.getParameter("balance"));
        int isPrivate = integer(req.getParameter("is_private"));
        if (id < 1 || !username.matches("[a-z0-9_.-]{3,64}") || balance == null || balance < 0
                || (isPrivate != 0 && isPrivate != 1)) {
            error(out, "User values are invalid.");
            return;
        }
        try (Connection conn = DatabaseManager.getConnection()) {
            conn.setAutoCommit(false);
            try (PreparedStatement update = conn.prepareStatement(
                    "UPDATE users SET username = ?, balance = ?, is_private = ? WHERE id = ?")) {
                String previousUsername = null;
                try (PreparedStatement find = conn.prepareStatement("SELECT username FROM users WHERE id = ?")) {
                    find.setInt(1, id);
                    try (ResultSet rs = find.executeQuery()) {
                        if (rs.next()) previousUsername = rs.getString(1);
                    }
                }
                if (previousUsername == null) {
                    conn.rollback();
                    error(out, "User not found.");
                    return;
                }
                update.setString(1, username);
                update.setDouble(2, balance);
                update.setInt(3, isPrivate);
                update.setInt(4, id);
                update.executeUpdate();
                try (PreparedStatement rename = conn.prepareStatement(
                        "UPDATE transactions SET sender_username = ? WHERE LOWER(sender_username) = LOWER(?)")) {
                    rename.setString(1, username);
                    rename.setString(2, previousUsername);
                    rename.executeUpdate();
                }
                try (PreparedStatement rename = conn.prepareStatement(
                        "UPDATE transactions SET receiver_username = ? WHERE LOWER(receiver_username) = LOWER(?)")) {
                    rename.setString(1, username);
                    rename.setString(2, previousUsername);
                    rename.executeUpdate();
                }
                conn.commit();
                success(out, "User updated.");
            } catch (Exception e) {
                conn.rollback();
                error(out, "Could not update user. The username may already exist.");
            }
        } catch (Exception e) {
            error(out, "Database operation failed.");
        }
    }

    private void deleteUser(HttpServletRequest req, PrintWriter out) {
        String username = safe(req.getParameter("username"));
        if (username.isEmpty()) {
            error(out, "Username is required.");
            return;
        }
        try (Connection conn = DatabaseManager.getConnection()) {
            conn.setAutoCommit(false);
            try (PreparedStatement deleteTransactions = conn.prepareStatement(
                    "DELETE FROM transactions WHERE LOWER(sender_username) = LOWER(?) OR LOWER(receiver_username) = LOWER(?)");
                 PreparedStatement deleteUser = conn.prepareStatement(
                         "DELETE FROM users WHERE LOWER(username) = LOWER(?)")) {
                deleteTransactions.setString(1, username);
                deleteTransactions.setString(2, username);
                deleteTransactions.executeUpdate();
                deleteUser.setString(1, username);
                int removed = deleteUser.executeUpdate();
                if (removed == 0) {
                    conn.rollback();
                    error(out, "User not found.");
                    return;
                }
                conn.commit();
                success(out, "User and associated transaction records removed.");
            } catch (Exception e) {
                conn.rollback();
                error(out, "Could not remove user.");
            }
        } catch (Exception e) {
            error(out, "Database operation failed.");
        }
    }

    private void updateTransaction(HttpServletRequest req, PrintWriter out) {
        int id = integer(req.getParameter("id"));
        String sender = safe(req.getParameter("sender"));
        String receiver = safe(req.getParameter("receiver"));
        Double amount = decimal(req.getParameter("amount"));
        if (id < 1 || sender.isEmpty() || receiver.isEmpty() || amount == null || amount <= 0) {
            error(out, "Transaction values are invalid.");
            return;
        }
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                     "UPDATE transactions SET sender_username = ?, receiver_username = ?, amount = ? WHERE id = ?")) {
            stmt.setString(1, sender);
            stmt.setString(2, receiver);
            stmt.setDouble(3, amount);
            stmt.setInt(4, id);
            if (stmt.executeUpdate() == 0) error(out, "Transaction not found.");
            else success(out, "Transaction updated. Wallet balances were not recalculated.");
        } catch (Exception e) {
            error(out, "Could not update transaction.");
        }
    }

    private void deleteTransaction(HttpServletRequest req, PrintWriter out) {
        int id = integer(req.getParameter("id"));
        if (id < 1) {
            error(out, "Transaction id is invalid.");
            return;
        }
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement("DELETE FROM transactions WHERE id = ?")) {
            stmt.setInt(1, id);
            if (stmt.executeUpdate() == 0) error(out, "Transaction not found.");
            else success(out, "Transaction removed.");
        } catch (Exception e) {
            error(out, "Could not remove transaction.");
        }
    }

    private boolean isAdmin(HttpServletRequest req) {
        HttpSession session = req.getSession(false);
        return session != null && Boolean.TRUE.equals(session.getAttribute(ADMIN_SESSION_KEY));
    }

    private int count(Statement stmt, String sql) throws Exception {
        try (ResultSet rs = stmt.executeQuery(sql)) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }

    private String configuredValue(String property, String environment) {
        String value = System.getProperty(property);
        if (value == null || value.trim().isEmpty()) value = System.getenv(environment);
        return value == null || value.trim().isEmpty() ? null : value.trim();
    }

    private String safe(String value) {
        return value == null ? "" : value.trim();
    }

    private int integer(String value) {
        try {
            return Integer.parseInt(safe(value));
        } catch (NumberFormatException e) {
            return -1;
        }
    }

    private Double decimal(String value) {
        try {
            double parsed = Double.parseDouble(safe(value));
            return Double.isFinite(parsed) ? parsed : null;
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private String escapeJson(String value) {
        if (value == null) return "";
        return value.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t");
    }

    private void prepareJson(HttpServletResponse resp) {
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        resp.setHeader("Cache-Control", "no-store");
    }

    private void success(PrintWriter out, String message) {
        out.print("{\"success\":true,\"message\":\"" + escapeJson(message) + "\"}");
    }

    private void error(PrintWriter out, String message) {
        out.print("{\"success\":false,\"message\":\"" + escapeJson(message) + "\"}");
    }

    private void forbidden(PrintWriter out) {
        error(out, "Administrator authentication required.");
    }
}
