java_code = '''package com.bitforge;

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
            // Recreate users table with username
            stmt.execute("CREATE TABLE IF NOT EXISTS users (" +
                    "id INT AUTO_INCREMENT PRIMARY KEY, " +
                    "username VARCHAR(255) UNIQUE NOT NULL, " +
                    "password_hash VARCHAR(255) NOT NULL, " +
                    "secret_question VARCHAR(255) NOT NULL, " +
                    "secret_answer VARCHAR(255) NOT NULL, " +
                    "balance DOUBLE DEFAULT 100.0, " +
                    "is_private TINYINT DEFAULT 0" +
                    ")");

            // Migration check if converting existing column
            try {
                stmt.execute("ALTER TABLE users CHANGE COLUMN email username VARCHAR(255) UNIQUE NOT NULL");
            } catch (Exception ignored) {}

            try {
                stmt.execute("ALTER TABLE users ADD COLUMN is_private TINYINT DEFAULT 0");
            } catch (Exception ignored) {}

            // Recreate transactions table with sender_username & receiver_username
            stmt.execute("CREATE TABLE IF NOT EXISTS transactions (" +
                    "id INT AUTO_INCREMENT PRIMARY KEY, " +
                    "sender_username VARCHAR(255) NOT NULL, " +
                    "receiver_username VARCHAR(255) NOT NULL, " +
                    "amount DOUBLE NOT NULL, " +
                    "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                    ")");

            try {
                stmt.execute("ALTER TABLE transactions CHANGE COLUMN sender_email sender_username VARCHAR(255) NOT NULL");
                stmt.execute("ALTER TABLE transactions CHANGE COLUMN receiver_email receiver_username VARCHAR(255) NOT NULL");
            } catch (Exception ignored) {}

            // Recreate blockchain table
            stmt.execute("CREATE TABLE IF NOT EXISTS blockchain (" +
                    "block_index INT PRIMARY KEY, " +
                    "previous_hash VARCHAR(255) NOT NULL, " +
                    "current_hash VARCHAR(255) NOT NULL, " +
                    "nonce INT NOT NULL, " +
                    "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " +
                    "transactions_data TEXT NOT NULL" +
                    ")");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void resetAllData() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("SET FOREIGN_KEY_CHECKS = 0");
            stmt.execute("TRUNCATE TABLE transactions");
            stmt.execute("TRUNCATE TABLE blockchain");
            stmt.execute("TRUNCATE TABLE users");
            stmt.execute("SET FOREIGN_KEY_CHECKS = 1");

            // Re-insert clean Genesis Block
            stmt.execute("INSERT INTO blockchain (block_index, previous_hash, current_hash, nonce, transactions_data) " +
                    "VALUES (1, '00000000000000000000000000000000', '0000a1b2c3d4e5f67890123456789012', 0, 'Genesis Block')");

            System.out.println("All database records cleared successfully!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        initDatabase();
        resetAllData();
    }
}
'''

with open("src/com/bitforge/DatabaseManager.java", "w") as f:
    f.write(java_code)
print("DatabaseManager.java updated with username fields & reset function!")
