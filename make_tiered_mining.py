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
            out.print("{\\"success\\": false, \\"message\\": \\"Miner email required.\\"}");
            return;
        }

        miner = miner.trim().toLowerCase();

        // 1. Detect Hardware Capabilities
        int cores = Runtime.getRuntime().availableProcessors();
        long maxMemoryMB = Runtime.getRuntime().maxMemory() / (1024 * 1024);

        int delayMillis;
        double rewardAmount;
        String hardwareTier;

        if (cores >= 8) {
            delayMillis = 1500;
            rewardAmount = 25.0; // High-end rig reward
            hardwareTier = "High Performance (" + cores + " Cores / " + maxMemoryMB + "MB RAM)";
        } else if (cores >= 4) {
            delayMillis = 4500;
            rewardAmount = 15.0; // Standard workstation reward
            hardwareTier = "Standard Performance (" + cores + " Cores / " + maxMemoryMB + "MB RAM)";
        } else {
            delayMillis = 9000;
            rewardAmount = 5.0;  // Entry-level reward
            hardwareTier = "Low Power (" + cores + " Cores / " + maxMemoryMB + "MB RAM)";
        }

        // 2. Simulate Hardware Processing Delay
        try {
            Thread.sleep(delayMillis);
        } catch (InterruptedException ignored) {}

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
            
            // 3. Insert Block into Blockchain
            PreparedStatement addBlock = conn.prepareStatement("INSERT INTO blockchain (block_index, previous_hash, current_hash, nonce, transactions_data) VALUES (?, ?, ?, ?, ?)");
            addBlock.setInt(1, nextIndex);
            addBlock.setString(2, prevHash);
            addBlock.setString(3, currentHash);
            addBlock.setInt(4, (int)(Math.random() * 100000));
            addBlock.setString(5, String.format("Block #%d [%s] Reward: %.2f BFG -> %s", nextIndex, hardwareTier, rewardAmount, miner));
            addBlock.executeUpdate();

            // 4. Update User Wallet Balance with Tiered Reward
            PreparedStatement reward = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE LOWER(email) = ?");
            reward.setDouble(1, rewardAmount);
            reward.setString(2, miner);
            reward.executeUpdate();

            // 5. Log Dynamic Reward into Transactions Ledger
            PreparedStatement logTx = conn.prepareStatement("INSERT INTO transactions (sender_email, receiver_email, amount) VALUES (?, ?, ?)");
            logTx.setString(1, "Mining Reward");
            logTx.setString(2, miner);
            logTx.setDouble(3, rewardAmount);
            logTx.executeUpdate();

            conn.commit();
            out.print(String.format("{\\"success\\": true, \\"block\\": %d, \\"tier\\": \\"%s\\", \\"reward\\": %.2f, \\"message\\": \\"Block #%d mined on %s! Received dynamic reward of +%.2f BFG!\\"}", nextIndex, hardwareTier, rewardAmount, nextIndex, hardwareTier, rewardAmount));
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Mining operation failed.\\"}");
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
print("MiningServlet.java updated with spec-based tiered rewards!")
