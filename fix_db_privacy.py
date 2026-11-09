code = '''package com.bitforge;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseManager {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/bitforge_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";
    private static final String USER = "bitforge";
    private static final String PASS = "bitforge123";

    public static Connection getConnection() throws SQLException, ClassNotFoundException {
        Class.forName("com.mysql.cj.jdbc.Driver");
        return DriverManager.getConnection(DB_URL, USER, PASS);
    }

    public static void initDatabase() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("CREATE TABLE IF NOT EXISTS users (" +
                    "id INT AUTO_INCREMENT PRIMARY KEY, " +
                    "email VARCHAR(255) UNIQUE NOT NULL, " +
                    "password_hash VARCHAR(255) NOT NULL, " +
                    "secret_question VARCHAR(255) NOT NULL, " +
                    "secret_answer VARCHAR(255) NOT NULL, " +
                    "balance DOUBLE DEFAULT 100.0, " +
                    "is_private TINYINT DEFAULT 0" +
                    ")");

            try {
                stmt.execute("ALTER TABLE users ADD COLUMN is_private TINYINT DEFAULT 0");
            } catch (Exception ignored) {}

            stmt.execute("CREATE TABLE IF NOT EXISTS transactions (" +
                    "id INT AUTO_INCREMENT PRIMARY KEY, " +
                    "sender_email VARCHAR(255) NOT NULL, " +
                    "receiver_email VARCHAR(255) NOT NULL, " +
                    "amount DOUBLE NOT NULL, " +
                    "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                    ")");

            stmt.execute("CREATE TABLE IF NOT EXISTS blockchain (" +
                    "block_index INT PRIMARY KEY, " +
                    "previous_hash VARCHAR(255) NOT NULL, " +
                    "current_hash VARCHAR(255) NOT NULL, " +
                    "nonce INT NOT NULL, " +
                    "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " +
                    "transactions_data TEXT NOT NULL" +
                    ")");

            stmt.execute("INSERT IGNORE INTO blockchain (block_index, previous_hash, current_hash, nonce, transactions_data) " +
                    "VALUES (1, '00000000000000000000000000000000', '0000a1b2c3d4e5f67890123456789012', 0, 'Genesis Block')");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
'''

with open("src/com/bitforge/DatabaseManager.java", "w") as f:
    f.write(code)
print("DatabaseManager.java updated with is_private column!")
