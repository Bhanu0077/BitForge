code = '''package com.bitforge;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.io.PrintWriter;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

@WebServlet("/api/auth/*")
public class AuthServlet extends HttpServlet {

    @Override
    public void init() throws ServletException {
        DatabaseManager.initDatabase();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getPathInfo();
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        if ("/signup".equals(path)) {
            handleSignup(req, out);
        } else if ("/login".equals(path)) {
            handleLogin(req, resp, out);
        } else if ("/forgot-password".equals(path)) {
            handleForgotPassword(req, out);
        } else {
            out.print("{\\"success\\": false, \\"message\\": \\"Invalid Auth Endpoint\\"}");
        }
    }

    private void handleSignup(HttpServletRequest req, PrintWriter out) {
        String email = req.getParameter("email");
        String password = req.getParameter("password");
        String question = req.getParameter("question");
        String answer = req.getParameter("answer");

        if (email == null || password == null || question == null || answer == null) {
            out.print("{\\"success\\": false, \\"message\\": \\"Missing required fields.\\"}");
            return;
        }

        try (Connection conn = DatabaseManager.getConnection()) {
            String sql = "INSERT INTO users (email, password_hash, secret_question, secret_answer, balance) VALUES (?, ?, ?, ?, 100.0)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, email);
            stmt.setString(2, hashPassword(password));
            stmt.setString(3, question);
            stmt.setString(4, answer.toLowerCase().trim());
            stmt.executeUpdate();

            out.print("{\\"success\\": true, \\"message\\": \\"User registered successfully!\\"}");
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Email already registered or database error.\\"}");
        }
    }

    private void handleLogin(HttpServletRequest req, HttpServletResponse resp, PrintWriter out) {
        String email = req.getParameter("email");
        String password = req.getParameter("password");

        try (Connection conn = DatabaseManager.getConnection()) {
            String sql = "SELECT email, balance FROM users WHERE email = ? AND password_hash = ?";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, email);
            stmt.setString(2, hashPassword(password));
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                HttpSession session = req.getSession(true);
                session.setAttribute("user", email);
                out.print(String.format("{\\"success\\": true, \\"email\\": \\"%s\\", \\"balance\\": %.2f}", email, rs.getDouble("balance")));
            } else {
                out.print("{\\"success\\": false, \\"message\\": \\"Invalid email or password.\\"}");
            }
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Login operation failed.\\"}");
        }
    }

    private void handleForgotPassword(HttpServletRequest req, PrintWriter out) {
        String email = req.getParameter("email");
        String answer = req.getParameter("answer");
        String newPassword = req.getParameter("new_password");

        try (Connection conn = DatabaseManager.getConnection()) {
            String sql = "SELECT secret_answer FROM users WHERE email = ?";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();

            if (rs.next() && rs.getString("secret_answer").equalsIgnoreCase(answer.trim())) {
                String updateSql = "UPDATE users SET password_hash = ? WHERE email = ?";
                PreparedStatement updateStmt = conn.prepareStatement(updateSql);
                updateStmt.setString(1, hashPassword(newPassword));
                updateStmt.setString(2, email);
                updateStmt.executeUpdate();

                out.print("{\\"success\\": true, \\"message\\": \\"Password reset successful!\\"}");
            } else {
                out.print("{\\"success\\": false, \\"message\\": \\"Verification failed. Incorrect secret answer.\\"}");
            }
        } catch (Exception e) {
            out.print("{\\"success\\": false, \\"message\\": \\"Password reset operation failed.\\"}");
        }
    }

    private String hashPassword(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(password.getBytes("UTF-8"));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            return password;
        }
    }
}
'''
with open("src/com/bitforge/AuthServlet.java", "w") as f:
    f.write(code)
print("src/com/bitforge/AuthServlet.java generated!")
