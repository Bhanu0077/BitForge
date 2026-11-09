code = '''package com.bitforge;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

@WebServlet("/api/mine/*")
public class MiningServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String miner = req.getParameter("miner");

        if (miner == null || miner.trim().isEmpty()) {
            out.print("{\"success\": false, \"message\": \"Miner email required.\"}");
            return;
        }

        miner = miner.trim().toLowerCase();

        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            conn.setAutoCommit(false);

            ResultSet rsLast = stmt.executeQuery("SELECT block_index, current_hash FROM blockchain ORDER BY block_index DESC LIMIT 1");
            
            int nextIndex = 1;
            String prevHash = "00000000000000000000000000000000";
            if (rsLast.next()) {
                nextIndex = rsLast.getInt("block_index") + 1;
                prevHash = rsLast.getString("current_hash");
            }

            String currentHash = hashInput("block_" + nextIndex + "_" + System.currentTimeMillis());
            
            // 1. Save Mined Block to Blockchain
            PreparedStatement addBlock = conn.prepareStatement("INSERT INTO blockchain (block_index, previous_hash, current_hash, nonce, transactions_data) VALUES (?, ?, ?, ?, ?)");
            addBlock.setInt(1, nextIndex);
            addBlock.setString(2, prevHash);
            addBlock.setString(3, currentHash);
            addBlock.setInt(4, (int)(Math.random() * 100000));
            addBlock.setString(5, "Mined Block #" + nextIndex + " Reward -> " + miner);
            addBlock.executeUpdate();

            // 2. Update User Balance in Database (+10 BFG)
            PreparedStatement reward = conn.prepareStatement("UPDATE users SET balance = balance + 10 WHERE LOWER(email) = ?");
            reward.setString(1, miner);
            reward.executeUpdate();

            // 3. Log Reward into Transactions Ledger
            PreparedStatement logTx = conn.prepareStatement("INSERT INTO transactions (sender_email, receiver_email, amount) VALUES (?, ?, ?)");
            logTx.setString(1, "Mining Reward");
            logTx.setString(2, miner);
            logTx.setDouble(3, 10.0);
            logTx.executeUpdate();

            conn.commit();
            out.print(String.format("{\"success\": true, \"block\": %d, \"message\": \"Block #%d mined! 10 BFG reward credited to your wallet.\"}", nextIndex, nextIndex));
        } catch (Exception e) {
            out.print("{\"success\": false, \"message\": \"Mining operation failed: " + e.getMessage() + "\"}");
        }
    }

    private String hashInput(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes("UTF-8"));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            return input;
        }
    }
}
'''

with open("src/com/bitforge/MiningServlet.java", "w") as f:
    f.write(code)
print("MiningServlet.java updated to register rewards into transactions ledger!")
