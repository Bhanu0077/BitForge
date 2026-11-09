package com.bitforge;

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
                txsJson.append(String.format("{\"from\":\"%s\",\"to\":\"%s\",\"amount\":%.2f,\"time\":\"%s\"},",
                        rsTxs.getString("sender_username"), rsTxs.getString("receiver_username"),
                        rsTxs.getDouble("amount"), rsTxs.getTimestamp("timestamp").toString()));
            }
            if (txsJson.length() > 1) txsJson.deleteCharAt(txsJson.length() - 1);

            ResultSet rsUsers = stmt.executeQuery("SELECT username FROM users");
            while (rsUsers.next()) {
                usersJson.append(String.format("{\"username\":\"%s\"},", rsUsers.getString("username")));
            }
            if (usersJson.length() > 1) usersJson.deleteCharAt(usersJson.length() - 1);

        } catch (Exception ignored) {}

        txsJson.append("]");
        usersJson.append("]");

        out.print(String.format("{\"success\": true, \"transactions\": %s, \"users\": %s}", txsJson.toString(), usersJson.toString()));
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
            out.print("{\"success\": false, \"message\": \"Invalid amount\"}");
            return;
        }

        if (sender == null || receiver == null || amount <= 0) {
            out.print("{\"success\": false, \"message\": \"Invalid parameters\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            conn.setAutoCommit(false);

            PreparedStatement checkBal = conn.prepareStatement("SELECT balance FROM users WHERE LOWER(username) = LOWER(?)");
            checkBal.setString(1, sender.trim());
            ResultSet rs = checkBal.executeQuery();

            if (!rs.next() || rs.getDouble("balance") < amount) {
                conn.rollback();
                out.print("{\"success\": false, \"message\": \"Insufficient account balance!\"}");
                return;
            }

            PreparedStatement checkRec = conn.prepareStatement("SELECT balance FROM users WHERE LOWER(username) = LOWER(?)");
            checkRec.setString(1, receiver.trim());
            if (!checkRec.executeQuery().next()) {
                conn.rollback();
                out.print("{\"success\": false, \"message\": \"Receiver username not found!\"}");
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
            out.print("{\"success\": true, \"message\": \"Transfer successful!\"}");

        } catch (Exception e) {
            out.print("{\"success\": false, \"message\": \"Transaction error\"}");
        }
    }
}
