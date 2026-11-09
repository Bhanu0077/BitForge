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

@WebServlet("/api/transactions/*")
public class TransactionServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("PRAGMA journal_mode=WAL;");
            stmt.execute("PRAGMA busy_timeout=5000;");

            ResultSet rsTxs = stmt.executeQuery("SELECT sender_email, receiver_email, amount, timestamp FROM transactions ORDER BY id DESC LIMIT 50");
            StringBuilder txsJson = new StringBuilder("[");
            while (rsTxs.next()) {
                txsJson.append(String.format("{\\"from\\":\\"%s\\",\\"to\\":\\"%s\\",\\"amount\\":%.2f,\\"time\\":\\"%s\\"},",
                    rsTxs.getString("sender_email"), rsTxs.getString("receiver_email"),
                    rsTxs.getDouble("amount"), rsTxs.getString("timestamp")));
            }
            if (txsJson.length() > 1) txsJson.deleteCharAt(txsJson.length() - 1);
            txsJson.append("]");

            ResultSet rsBlocks = stmt.executeQuery("SELECT block_index, current_hash, previous_hash, transactions_data, timestamp FROM blockchain ORDER BY block_index DESC");
            StringBuilder blocksJson = new StringBuilder("[");
            while (rsBlocks.next()) {
                blocksJson.append(String.format("{\\"index\\":%d,\\"hash\\":\\"%s\\",\\"prev\\":\\"%s\\",\\"data\\":\\"%s\\",\\"time\\":\\"%s\\"},",
                    rsBlocks.getInt("block_index"), rsBlocks.getString("current_hash"),
                    rsBlocks.getString("previous_hash"), rsBlocks.getString("transactions_data"),
                    rsBlocks.getString("timestamp")));
            }
            if (blocksJson.length() > 1) blocksJson.deleteCharAt(blocksJson.length() - 1);
            blocksJson.append("]");

            out.print(String.format("{\\"transactions\\": %s, \\"blocks\\": %s}", txsJson.toString(), blocksJson.toString()));
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Database sync error\\"}");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        String sender = req.getParameter("sender");
        String receiver = req.getParameter("receiver");
        String amountStr = req.getParameter("amount");

        if (sender == null || receiver == null || amountStr == null) {
            out.print("{\\"success\\": false, \\"message\\": \\"Missing payment parameters.\\"}");
            return;
        }

        sender = sender.trim();
        receiver = receiver.trim();

        double amount;
        try {
            amount = Double.parseDouble(amountStr);
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid payment amount.\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection(); Statement setupStmt = conn.createStatement()) {
            setupStmt.execute("PRAGMA journal_mode=WAL;");
            setupStmt.execute("PRAGMA busy_timeout=5000;");

            conn.setAutoCommit(false);

            // Check Sender Balance
            PreparedStatement checkSender = conn.prepareStatement("SELECT balance FROM users WHERE email = ? COLLATE NOCASE");
            checkSender.setString(1, sender);
            ResultSet rs = checkSender.executeQuery();
            if (!rs.next()) {
                conn.rollback();
                out.print("{\\"success\\": false, \\"message\\": \\"Sender account not found in database.\\"}");
                return;
            }

            double senderBalance = rs.getDouble("balance");
            if (senderBalance < amount) {
                conn.rollback();
                out.print(String.format("{\\"success\\": false, \\"message\\": \\"Insufficient balance! Available: %.2f BFG\\"} ", senderBalance));
                return;
            }

            // Check Receiver Exists
            PreparedStatement checkReceiver = conn.prepareStatement("SELECT balance FROM users WHERE email = ? COLLATE NOCASE");
            checkReceiver.setString(1, receiver);
            ResultSet rsRec = checkReceiver.executeQuery();
            if (!rsRec.next()) {
                conn.rollback();
                out.print(String.format("{\\"success\\": false, \\"message\\": \\"Receiver account '%s' does not exist in BitForge ecosystem.\\"}", receiver));
                return;
            }

            // Deduct Sender Balance
            PreparedStatement deduct = conn.prepareStatement("UPDATE users SET balance = balance - ? WHERE email = ? COLLATE NOCASE");
            deduct.setDouble(1, amount);
            deduct.setString(2, sender);
            deduct.executeUpdate();

            // Credit Receiver Balance
            PreparedStatement credit = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE email = ? COLLATE NOCASE");
            credit.setDouble(1, amount);
            credit.setString(2, receiver);
            credit.executeUpdate();

            // Record Transaction
            PreparedStatement logTx = conn.prepareStatement("INSERT INTO transactions (sender_email, receiver_email, amount) VALUES (?, ?, ?)");
            logTx.setString(1, sender);
            logTx.setString(2, receiver);
            logTx.setDouble(3, amount);
            logTx.executeUpdate();

            conn.commit();
            out.print(String.format("{\\"success\\": true, \\"message\\": \\"Successfully sent %.2f BFG to %s!\\"} ", amount, receiver));
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Transaction processing failed due to DB lock or timeout.\\"}");
        }
    }
}
'''

with open("src/com/bitforge/TransactionServlet.java", "w") as f:
    f.write(code)
print("src/com/bitforge/TransactionServlet.java updated successfully!")
