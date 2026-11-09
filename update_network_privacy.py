code = '''package com.bitforge;

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

@WebServlet("/api/network/*")
public class NetworkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        StringBuilder peersJson = new StringBuilder("[");
        int userCount = 0;
        int txCount = 0;
        int blockCount = 0;

        try (Connection conn = DatabaseManager.getConnection(); Statement stmt = conn.createStatement()) {
            ResultSet rsUsers = stmt.executeQuery("SELECT email, balance, is_private FROM users ORDER BY id DESC");
            while (rsUsers.next()) {
                userCount++;
                boolean isPrivate = rsUsers.getInt("is_private") == 1;
                double balance = isPrivate ? -1.0 : rsUsers.getDouble("balance");

                peersJson.append(String.format("{\\"email\\":\\"%s\\",\\"balance\\":%.2f,\\"is_private\\":%b},",
                    rsUsers.getString("email"), balance, isPrivate));
            }
            if (peersJson.length() > 1) peersJson.deleteCharAt(peersJson.length() - 1);

            ResultSet rsTxs = stmt.executeQuery("SELECT COUNT(*) FROM transactions");
            if (rsTxs.next()) txCount = rsTxs.getInt(1);

            ResultSet rsBlocks = stmt.executeQuery("SELECT COUNT(*) FROM blockchain");
            if (rsBlocks.next()) blockCount = rsBlocks.getInt(1);
        } catch (Exception e) {
            // DB fallback
        }
        peersJson.append("]");

        int cores = Runtime.getRuntime().availableProcessors();
        long freeMemMB = Runtime.getRuntime().freeMemory() / (1024 * 1024);

        String json = String.format(
            "{\\"success\\": true, \\"users\\": %d, \\"transactions\\": %d, \\"blocks\\": %d, \\"cores\\": %d, \\"freeMemMB\\": %d, \\"javaVersion\\": \\"%s\\", \\"peers\\": %s}",
            userCount, txCount, blockCount, cores, freeMemMB, System.getProperty("java.version"), peersJson.toString()
        );

        out.print(json);
    }
}
'''

with open("src/com/bitforge/NetworkServlet.java", "w") as f:
    f.write(code)
print("NetworkServlet.java updated to enforce privacy!")
