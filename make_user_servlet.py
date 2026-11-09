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

@WebServlet("/api/user/*")
public class UserServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String email = req.getParameter("email");

        if (email == null || email.trim().isEmpty()) {
            out.print("{\\"success\\": false, \\"message\\": \\"Email required\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            PreparedStatement pstmt = conn.prepareStatement("SELECT balance, is_private FROM users WHERE LOWER(email) = LOWER(?)");
            pstmt.setString(1, email.trim());
            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                double balance = rs.getDouble("balance");
                boolean isPrivate = rs.getInt("is_private") == 1;
                out.print(String.format("{\\"success\\": true, \\"balance\\": %.2f, \\"is_private\\": %b}", balance, isPrivate));
            } else {
                out.print("{\\"success\\": false, \\"message\\": \\"User not found\\"}");
            }
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"DB error\\"}");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String email = req.getParameter("email");
        String toggle = req.getParameter("toggle");

        if (email == null || toggle == null) {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid params\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            PreparedStatement pstmt = conn.prepareStatement("UPDATE users SET is_private = ? WHERE LOWER(email) = LOWER(?)");
            pstmt.setInt(1, "true".equalsIgnoreCase(toggle) ? 1 : 0);
            pstmt.setString(2, email.trim());
            pstmt.executeUpdate();

            out.print("{\\"success\\": true}");
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"DB update error\\"}");
        }
    }
}
'''

with open("src/com/bitforge/UserServlet.java", "w") as f:
    f.write(code)
print("UserServlet.java created!")
