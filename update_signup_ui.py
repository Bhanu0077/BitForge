signup_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Sign Up</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .pwd-container { position: relative; display: flex; align-items: center; }
        .pwd-container input { width: 100%; padding-right: 40px; }
        .toggle-pwd { position: absolute; right: 10px; cursor: pointer; user-select: none; font-size: 1.2rem; }
    </style>
</head>
<body>
    <div class="auth-container" style="max-width: 450px; margin: 50px auto; padding: 25px; border: 1px solid #00d2ff; border-radius: 10px;">
        <h2 style="text-align: center;">Join BitForge Ecosystem</h2>
        <form id="signupForm" onsubmit="handleSignup(event)">
            <label>Email Address</label>
            <input type="email" id="signupEmail" required placeholder="user@bitforge.org" style="width: 100%; margin-bottom: 15px; padding: 10px;">

            <label>Password</label>
            <div class="pwd-container" style="margin-bottom: 15px;">
                <input type="password" id="signupPassword" required minlength="6" placeholder="Enter password">
                <span class="toggle-pwd" onclick="togglePasswordVisibility('signupPassword', this)">👁️</span>
            </div>

            <label>Confirm Password</label>
            <div class="pwd-container" style="margin-bottom: 15px;">
                <input type="password" id="signupConfirm" required minlength="6" placeholder="Confirm password">
                <span class="toggle-pwd" onclick="togglePasswordVisibility('signupConfirm', this)">👁️</span>
            </div>

            <label>Secret Security Question (For Recovery)</label>
            <select id="secretQuestion" required style="width: 100%; margin-bottom: 15px; padding: 10px; background: #1e1e1e; color: #fff;">
                <option value="pet">What is your favorite pet's name?</option>
                <option value="city">In what city were you born?</option>
                <option value="school">What was the name of your first school?</option>
            </select>

            <label>Secret Security Answer</label>
            <input type="text" id="secretAnswer" required placeholder="Your answer..." style="width: 100%; margin-bottom: 20px; padding: 10px;">

            <button type="submit" style="width: 100%; padding: 12px; background: #00d2ff; color: #000; font-weight: bold; border: none; cursor: pointer;">Create BitForge Account</button>
        </form>
        <div id="authMessage" class="message" style="margin-top: 15px; text-align: center;"></div>
        <p style="text-align: center; margin-top: 15px;">Already have an account? <a href="login.html" style="color: #00d2ff;">Login here</a></p>
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

with open("html/signup.html", "w") as f:
    f.write(signup_html)
print("html/signup.html updated!")
