import os

# 1. BlockchainServlet.java
blockchain_code = '''package com.bitforge;

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
                String safeData = rs.getString("transactions_data").replace("\"", "\\\"");
                blocksJson.append(String.format(
                    "{\"index\":%d,\"prev\":\"%s\",\"hash\":\"%s\",\"nonce\":%d,\"time\":\"%s\",\"data\":\"%s\"},",
                    rs.getInt("block_index"),
                    rs.getString("previous_hash"),
                    rs.getString("current_hash"),
                    rs.getInt("nonce"),
                    rs.getTimestamp("timestamp").toString(),
                    safeData
                ));
            }
            if (blocksJson.length() > 1) blocksJson.deleteCharAt(blocksJson.length() - 1);
        } catch (Exception ignored) {}

        blocksJson.append("]");
        out.print(String.format("{\"success\": true, \"blocks\": %s}", blocksJson.toString()));
    }
}
'''

# 2. MiningServlet.java
mining_code = '''package com.bitforge;

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

@WebServlet("/api/mining/*")
public class MiningServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        String username = req.getParameter("username");
        if (username == null || username.trim().isEmpty()) {
            username = req.getParameter("miner");
        }
        if (username == null || username.trim().isEmpty()) {
            username = req.getParameter("email");
        }

        double reward = 10.0;
        try {
            if (req.getParameter("reward") != null) {
                reward = Double.parseDouble(req.getParameter("reward"));
            }
        } catch (Exception ignored) {}

        if (username == null || username.trim().isEmpty()) {
            out.print("{\"success\": false, \"message\": \"Miner username required.\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            conn.setAutoCommit(false);

            PreparedStatement updateBal = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE LOWER(username) = LOWER(?)");
            updateBal.setDouble(1, reward);
            updateBal.setString(2, username.trim());
            int rowsUpdated = updateBal.executeUpdate();

            if (rowsUpdated == 0) {
                conn.rollback();
                out.print("{\"success\": false, \"message\": \"Miner user account not found.\"}");
                return;
            }

            int lastIndex = 1;
            String prevHash = "00000000000000000000000000000000";
            Statement stmt = conn.createStatement();
            ResultSet rsBlock = stmt.executeQuery("SELECT block_index, current_hash FROM blockchain ORDER BY block_index DESC LIMIT 1");
            if (rsBlock.next()) {
                lastIndex = rsBlock.getInt("block_index") + 1;
                prevHash = rsBlock.getString("current_hash");
            }

            int nonce = (int) (Math.random() * 90000) + 10000;
            String currentHash = String.format("0000%032x", System.currentTimeMillis() + nonce);
            String blockData = "Block #" + lastIndex + " Mined by " + username.trim() + " (+ " + reward + " BFG)";

            PreparedStatement addBlock = conn.prepareStatement(
                "INSERT INTO blockchain (block_index, previous_hash, current_hash, nonce, transactions_data) VALUES (?, ?, ?, ?, ?)"
            );
            addBlock.setInt(1, lastIndex);
            addBlock.setString(2, prevHash);
            addBlock.setString(3, currentHash);
            addBlock.setInt(4, nonce);
            addBlock.setString(5, blockData);
            addBlock.executeUpdate();

            conn.commit();
            out.print(String.format("{\"success\": true, \"message\": \"Block #%d successfully mined! Reward of %.2f BFG credited.\", \"hash\": \"%s\", \"nonce\": %d}", lastIndex, reward, currentHash, nonce));

        } catch (Exception e) {
            e.printStackTrace();
            out.print("{\"success\": false, \"message\": \"Mining database update failed.\"}");
        }
    }
}
'''

with open("src/com/bitforge/BlockchainServlet.java", "w") as f:
    f.write(blockchain_code)

with open("src/com/bitforge/MiningServlet.java", "w") as f:
    f.write(mining_code)

print("BlockchainServlet.java and MiningServlet.java fixed successfully!")
