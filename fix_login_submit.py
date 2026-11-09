login_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Login</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #0f172a;">
    <div style="background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #00d2ff; width: 90%; max-width: 400px; text-align: center;">
        <h2 style="color: #00d2ff; margin-bottom: 10px;">BitForge Login</h2>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 20px;">Access your blockchain wallet</p>

        <form id="loginForm" onsubmit="handleLogin(event)">
            <div style="margin-bottom: 15px; text-align: left;">
                <label style="font-size: 0.85rem; color: #94a3b8;">Email Address</label>
                <input type="email" id="loginEmail" required placeholder="name@example.com" style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #fff; margin-top: 5px;">
            </div>

            <div style="margin-bottom: 20px; text-align: left;">
                <label style="font-size: 0.85rem; color: #94a3b8;">Password</label>
                <input type="password" id="loginPassword" required placeholder="••••••••" style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #fff; margin-top: 5px;">
            </div>

            <button type="submit" style="width: 100%; padding: 12px; background: #00d2ff; color: #000; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem;">Login to Wallet</button>
        </form>

        <div id="authMessage" style="margin-top: 15px; font-size: 0.9rem; font-weight: bold;"></div>

        <div style="margin-top: 20px; font-size: 0.85rem;">
            <a href="signup.html" style="color: #00d2ff; text-decoration: none;">Create New Account</a> | 
            <a href="forgot-password.html" style="color: #94a3b8; text-decoration: none;">Forgot Password?</a>
        </div>
    </div>

    <script src="../script.js"></script>
</body>
</html>'''

with open("html/login.html", "w") as f:
    f.write(login_html)

print("html/login.html updated successfully!")
