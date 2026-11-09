package com.bitforge;

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
                String safeData = rs.getString("transactions_data").replace((char)34 + "", "\\" + (char)34);
                blocksJson.append("{\"index\":" + rs.getInt("block_index") + 
                    ",\"prev\":\"" + rs.getString("previous_hash") + 
                    "\",\"hash\":\"" + rs.getString("current_hash") + 
                    "\",\"nonce\":" + rs.getInt("nonce") + 
                    ",\"time\":\"" + rs.getTimestamp("timestamp").toString() + 
                    "\",\"data\":\"" + safeData + "\"},");
            }
            if (blocksJson.length() > 1) blocksJson.deleteCharAt(blocksJson.length() - 1);
        } catch (Exception ignored) {}
        blocksJson.append("]");
        out.print("{\"success\": true, \"blocks\": " + blocksJson.toString() + "}");
    }
}