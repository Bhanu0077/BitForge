code = '''package com.bitforge;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseManager {
    private static final String DB_URL = "jdbc:sqlite:" + System.getProperty("user.home") + "/BitForge/database/bitforge.db";

    public static Connection getConnection() throws SQLException, ClassNotFoundException {
        Class.forName("org.sqlite.JDBC");
        return DriverManager.getConnection(DB_URL);
    }

    public static void initDatabase() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            // Users table for Goal 1 & 2
            stmt.execute("CREATE TABLE IF NOT EXISTS users (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "email TEXT UNIQUE NOT NULL, " +
                    "password_hash TEXT NOT NULL, " +
                    "secret_question TEXT NOT NULL, " +
                    "secret_answer TEXT NOT NULL, " +
                    "balance REAL DEFAULT 100.0" +
                    ")");

            // Transactions table for Goal 2 & 3
            stmt.execute("CREATE TABLE IF NOT EXISTS transactions (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "sender_email TEXT NOT NULL, " +
                    "receiver_email TEXT NOT NULL, " +
                    "amount REAL NOT NULL, " +
                    "timestamp TEXT DEFAULT CURRENT_TIMESTAMP" +
                    ")");

            // Blockchain table for Goal 2
            stmt.execute("CREATE TABLE IF NOT EXISTS blockchain (" +
                    "block_index INTEGER PRIMARY KEY, " +
                    "previous_hash TEXT NOT NULL, " +
                    "current_hash TEXT NOT NULL, " +
                    "nonce INTEGER NOT NULL, " +
                    "timestamp TEXT DEFAULT CURRENT_TIMESTAMP, " +
                    "transactions_data TEXT NOT NULL" +
                    ")");

            // Seed Genesis Block if empty
            stmt.execute("INSERT OR IGNORE INTO blockchain (block_index, previous_hash, current_hash, nonce, transactions_data) " +
                    "VALUES (1, '00000000000000000000000000000000', '0000a1b2c3d4e5f67890123456789012', 0, 'Genesis Block')");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
'''
with open("src/com/bitforge/DatabaseManager.java", "w") as f:
    f.write(code)
print("src/com/bitforge/DatabaseManager.java generated!")
