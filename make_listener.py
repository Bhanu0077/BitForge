code = '''package com.bitforge;

import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;

@WebListener
public class AppContextListener implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        System.out.println("Initializing BitForge MySQL Schema...");
        DatabaseManager.initDatabase();
        System.out.println("BitForge MySQL Schema initialized successfully!");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
    }
}
'''
with open("src/com/bitforge/AppContextListener.java", "w") as f:
    f.write(code)
print("AppContextListener.java created!")
