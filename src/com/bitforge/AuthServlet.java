package com.bitforge;

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

@WebServlet("/api/auth/*")
public class AuthServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();
        String path = req.getPathInfo();

        if ("/signup".equals(path)) {
            String username = req.getParameter("username");
            String password = req.getParameter("password");
            String question = req.getParameter("question");
            String answer = req.getParameter("answer");

            if (username == null || password == null) {
                out.print("{\"success\": false, \"message\": \"Username and password required\"}");
                return;
            }

            try (Connection conn = DatabaseManager.getConnection()) {
                PreparedStatement pstmt = conn.prepareStatement(
                    "INSERT INTO users (username, password_hash, secret_question, secret_answer, balance) VALUES (?, ?, ?, ?, 100.0)"
                );
                pstmt.setString(1, username.trim().toLowerCase());
                pstmt.setString(2, password);
                pstmt.setString(3, question != null ? question : "default");
                pstmt.setString(4, answer != null ? answer : "default");
                pstmt.executeUpdate();

                out.print(String.format("{\"success\": true, \"message\": \"Account created successfully\", \"username\": \"%s\"}", username.trim().toLowerCase()));
            } catch (Exception e) {
                out.print("{\"success\": false, \"message\": \"Username already exists!\"}");
            }

        } else if ("/login".equals(path)) {
            String username = req.getParameter("username");
            String password = req.getParameter("password");

            try (Connection conn = DatabaseManager.getConnection()) {
                PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND password_hash = ?");
                pstmt.setString(1, username != null ? username.trim() : "");
                pstmt.setString(2, password);
                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    out.print(String.format("{\"success\": true, \"username\": \"%s\"}", rs.getString("username")));
                } else {
                    out.print("{\"success\": false, \"message\": \"Invalid username or password\"}");
                }
            } catch (Exception e) {
                out.print("{\"success\": false, \"message\": \"Database error\"}");
            }

        } else if ("/forgot-password".equals(path)) {
            String username = req.getParameter("username");
            String answer = req.getParameter("answer");
            String newPassword = req.getParameter("new_password");

            try (Connection conn = DatabaseManager.getConnection()) {
                PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND LOWER(secret_answer) = LOWER(?)");
                pstmt.setString(1, username != null ? username.trim() : "");
                pstmt.setString(2, answer != null ? answer.trim() : "");
                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    PreparedStatement updatePstmt = conn.prepareStatement("UPDATE users SET password_hash = ? WHERE LOWER(username) = LOWER(?)");
                    updatePstmt.setString(1, newPassword);
                    updatePstmt.setString(2, username.trim());
                    updatePstmt.executeUpdate();

                    out.print("{\"success\": true, \"message\": \"Password updated successfully!\"}");
                } else {
                    out.print("{\"success\": false, \"message\": \"Incorrect secret answer or username\"}");
                }
            } catch (Exception e) {
                out.print("{\"success\": false, \"message\": \"Recovery error\"}");
            }
        }
    }
}
