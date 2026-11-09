code = '''package com.bitforge;

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

            // 1. Credit block reward to miner's account balance
            PreparedStatement updateBal = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE LOWER(username) = LOWER(?)");
            updateBal.setDouble(1, reward);
            updateBal.setString(2, username.trim());
            int rowsUpdated = updateBal.executeUpdate();

            if (rowsUpdated == 0) {
                conn.rollback();
                out.print("{\"success\": false, \"message\": \"Miner user account not found.\"}");
                return;
            }

            // 2. Fetch latest block index and hash
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

            // 3. Append new block to blockchain table
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

with open("src/com/bitforge/MiningServlet.java", "w") as f:
    f.write(code)

print("MiningServlet.java updated to handle usernames!")
