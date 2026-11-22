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

@WebServlet("/api/blockchain/*")
public class BlockchainServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        StringBuilder blocksJson = new StringBuilder("[");
        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            ResultSet rs = stmt.executeQuery("SELECT block_index, previous_hash, current_hash, nonce, timestamp, transactions_data FROM blockchain ORDER BY block_index ASC");
            while (rs.next()) {
                int blockIndex = rs.getInt("block_index");
                StringBuilder transactionsJson = new StringBuilder("[");
                try (PreparedStatement txStmt = conn.prepareStatement("SELECT sender_username, receiver_username, amount, timestamp FROM transactions WHERE block_index = ? ORDER BY id ASC")) {
                    txStmt.setInt(1, blockIndex);
                    try (ResultSet txRs = txStmt.executeQuery()) {
                        while (txRs.next()) {
                            transactionsJson.append("{\"from\":\"").append(jsonEscape(txRs.getString("sender_username")))
                                .append("\",\"to\":\"").append(jsonEscape(txRs.getString("receiver_username")))
                                .append("\",\"amount\":").append(txRs.getDouble("amount"))
                                .append(",\"time\":\"").append(txRs.getTimestamp("timestamp").toString()).append("\"},");
                        }
                    }
                }
                if (transactionsJson.length() > 1) transactionsJson.deleteCharAt(transactionsJson.length() - 1);
                transactionsJson.append("]");

                String safeData = jsonEscape(rs.getString("transactions_data"));
                blocksJson.append("{\"index\":" + blockIndex +
                    ",\"prev\":\"" + jsonEscape(rs.getString("previous_hash")) +
                    "\",\"hash\":\"" + jsonEscape(rs.getString("current_hash")) +
                    "\",\"nonce\":" + rs.getInt("nonce") +
                    ",\"time\":\"" + rs.getTimestamp("timestamp").toString() +
                    "\",\"data\":\"" + safeData + "\",\"transactions\":" + transactionsJson + "},");
            }
            if (blocksJson.length() > 1) blocksJson.deleteCharAt(blocksJson.length() - 1);
        } catch (Exception ignored) {}
        blocksJson.append("]");
        out.print("{\"success\": true, \"blocks\": " + blocksJson.toString() + "}");
    }

    private String jsonEscape(String value) {
        if (value == null) return "";
        return value.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r");
    }
}