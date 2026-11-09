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
            ResultSet rsTxs = stmt.executeQuery("SELECT * FROM transactions ORDER BY id DESC LIMIT 50");
            StringBuilder txsJson = new StringBuilder("[");
            while (rsTxs.next()) {
                txsJson.append(String.format("{\\"from\\":\\"%s\\",\\"to\\":\\"%s\\",\\"amount\\":%.2f,\\"time\\":\\"%s\\"},",
                    rsTxs.getString("sender_email"), rsTxs.getString("receiver_email"),
                    rsTxs.getDouble("amount"), rsTxs.getString("timestamp")));
            }
            if (txsJson.length() > 1) txsJson.deleteCharAt(txsJson.length() - 1);
            txsJson.append("]");

            ResultSet rsBlocks = stmt.executeQuery("SELECT * FROM blockchain ORDER BY block_index DESC");
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

        sender = sender.trim().toLowerCase();
        receiver = receiver.trim().toLowerCase();

        double amount;
        try {
            amount = Double.parseDouble(amountStr);
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid payment amount.\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            conn.setAutoCommit(false);

            // Check Sender Balance
            PreparedStatement checkSender = conn.prepareStatement("SELECT balance FROM users WHERE LOWER(email) = ?");
            checkSender.setString(1, sender);
            ResultSet rs = checkSender.executeQuery();
            if (!rs.next()) {
                conn.rollback();
                out.print("{\\"success\\": false, \\"message\\": \\"Sender account not found in database.\\"}");
                return;
            }
            if (rs.getDouble("balance") < amount) {
                conn.rollback();
                out.print(String.format("{\\"success\\": false, \\"message\\": \\"Insufficient balance! Available: %.2f BFG\\"} ", rs.getDouble("balance")));
                return;
            }

            // Check Receiver Exists
            PreparedStatement checkReceiver = conn.prepareStatement("SELECT balance FROM users WHERE LOWER(email) = ?");
            checkReceiver.setString(1, receiver);
            if (!checkReceiver.executeQuery().next()) {
                conn.rollback();
                out.print(String.format("{\\"success\\": false, \\"message\\": \\"Receiver account '%s' does not exist in BitForge ecosystem. Please sign up receiver first.\\"}", receiver));
                return;
            }

            // Perform Deduct & Credit
            PreparedStatement deduct = conn.prepareStatement("UPDATE users SET balance = balance - ? WHERE LOWER(email) = ?");
            deduct.setDouble(1, amount);
            deduct.setString(2, sender);
            deduct.executeUpdate();

            PreparedStatement credit = conn.prepareStatement("UPDATE users SET balance = balance + ? WHERE LOWER(email) = ?");
            credit.setDouble(1, amount);
            credit.setString(2, receiver);
            credit.executeUpdate();

            PreparedStatement logTx = conn.prepareStatement("INSERT INTO transactions (sender_email, receiver_email, amount) VALUES (?, ?, ?)");
            logTx.setString(1, sender);
            logTx.setString(2, receiver);
            logTx.setDouble(3, amount);
            logTx.executeUpdate();

            conn.commit();
            out.print(String.format("{\\"success\\": true, \\"message\\": \\"Successfully sent %.2f BFG to %s!\\"} ", amount, receiver));
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Transaction DB processing error.\\"}");
        }
    }
}
'''
with open("src/com/bitforge/TransactionServlet.java", "w") as f:
    f.write(code)
print("src/com/bitforge/TransactionServlet.java syntax fixed!")
