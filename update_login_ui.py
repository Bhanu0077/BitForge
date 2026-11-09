login_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Login</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .pwd-container { position: relative; display: flex; align-items: center; }
        .pwd-container input { width: 100%; padding-right: 40px; }
        .toggle-pwd { position: absolute; right: 10px; cursor: pointer; user-select: none; font-size: 1.2rem; }
    </style>
</head>
<body>
    <div class="auth-container" style="max-width: 450px; margin: 50px auto; padding: 25px; border: 1px solid #00d2ff; border-radius: 10px;">
        <h2 style="text-align: center;">BitForge Login</h2>
        
        <!-- Standard Login Form -->
        <form id="loginForm" onsubmit="handleLogin(event)">
            <label>Email Address</label>
            <input type="email" id="loginEmail" required placeholder="user@bitforge.org" style="width: 100%; margin-bottom: 15px; padding: 10px;">

            <label>Password</label>
            <div class="pwd-container" style="margin-bottom: 20px;">
                <input type="password" id="loginPassword" required placeholder="Enter password">
                <span class="toggle-pwd" onclick="togglePasswordVisibility('loginPassword', this)">👁️</span>
            </div>

            <button type="submit" style="width: 100%; padding: 12px; background: #00d2ff; color: #000; font-weight: bold; border: none; cursor: pointer;">Login to Wallet</button>
        </form>

        <hr style="margin: 25px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.2);">

        <!-- Forgot Password / Secret Answer Reset Section -->
        <details>
            <summary style="cursor: pointer; color: #00d2ff; font-weight: bold; text-align: center;">Forgot Password?</summary>
            <form id="forgotForm" onsubmit="handleForgotPassword(event)" style="margin-top: 15px;">
                <label>Registered Email</label>
                <input type="email" id="forgotEmail" required placeholder="user@bitforge.org" style="width: 100%; margin-bottom: 10px; padding: 8px;">

                <label>Secret Security Answer</label>
                <input type="text" id="forgotAnswer" required placeholder="Your answer..." style="width: 100%; margin-bottom: 10px; padding: 8px;">

                <label>New Password</label>
                <div class="pwd-container" style="margin-bottom: 15px;">
                    <input type="password" id="forgotNewPassword" required minlength="6" placeholder="Enter new password">
                    <span class="toggle-pwd" onclick="togglePasswordVisibility('forgotNewPassword', this)">👁️</span>
                </div>

                <button type="submit" style="width: 100%; padding: 10px; background: #e74c3c; color: #fff; border: none; cursor: pointer; font-weight: bold;">Reset Password</button>
            </form>
        </details>

        <div id="authMessage" class="message" style="margin-top: 15px; text-align: center;"></div>
        <p style="text-align: center; margin-top: 15px;">Don't have an account? <a href="signup.html" style="color: #00d2ff;">Sign Up</a></p>
    </div>

    <script src="../script.js"></script>
    <script>
        function togglePasswordVisibility(fieldId, btn) {
            const field = document.getElementById(fieldId);
            if (field.type === "password") {
                field.type = "text";
                btn.textContent = "🙈";
            } else {
                field.type = "password";
                btn.textContent = "👁️";
            }
        }
    </script>
</body>
</html>'''

with open("html/login.html", "w") as f:
    f.write(login_html)
print("html/login.html updated!")
