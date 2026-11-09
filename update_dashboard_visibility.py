dash_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Central Dashboard</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
        .stat-card { border: 1px solid #00d2ff; padding: 20px; border-radius: 10px; background: rgba(0, 210, 255, 0.05); position: relative; }
        .action-btn { display: inline-block; padding: 10px 20px; background: #00d2ff; color: #000; font-weight: bold; text-decoration: none; border-radius: 5px; margin-top: 10px; }
        .toggle-btn { padding: 6px 14px; background: #34495e; color: #fff; border: 1px solid #00d2ff; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 0.85rem; margin-top: 8px; }
        .toggle-btn.private { background: #e74c3c; border-color: #e74c3c; }
    </style>
</head>
<body>
    <nav>
        <a href="index.html" class="active">Dashboard</a>
        <a href="wallet.html">Wallet</a>
        <a href="transactions.html">Transactions / Pay</a>
        <a href="mining.html">Mining</a>
        <a href="blockchain.html">Ledger</a>
        <a href="network.html">Network</a>
        <button onclick="logout()" style="background: #e74c3c; padding: 5px 15px; border: none; cursor: pointer;">Logout</button>
    </nav>

    <div class="container" style="padding: 20px;">
        <h2>Welcome to BitForge Platform</h2>
        <p>Logged in as: <strong data-user style="color: #00d2ff;">Loading...</strong></p>

        <div class="grid-3">
            <div class="stat-card">
                <h3>Available Balance</h3>
                <h1 style="color: #2ecc71;"><span id="userBalance">0.00</span> BFG</h1>
                
                <!-- Visibility Control Button -->
                <div>
                    <button id="visibilityBtn" class="toggle-btn" onclick="toggleBalanceVisibility()">👁️ Visibility: Public</button>
                </div>
                
                <a href="transactions.html" class="action-btn">Send & Receive Coins</a>
            </div>

            <div class="stat-card">
                <h3>Proof-of-Work Mining</h3>
                <p>Dynamic hardware-tier block rewards ready.</p>
                <a href="mining.html" class="action-btn" style="background: #27ae60; color: #fff;">⚡ Mine Blocks Now</a>
            </div>

            <div class="stat-card">
                <h3>Immutable Blockchain</h3>
                <p>Total Mined Blocks: <strong data-blocks style="color: #00d2ff;">1</strong></p>
                <a href="blockchain.html" class="action-btn" style="background: #8e44ad; color: #fff;">Explore Blockchain Ledger</a>
            </div>
        </div>

        <h3 style="margin-top: 40px;">Recent Ecosystem Activity</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
            <thead>
                <tr style="border-bottom: 2px solid #00d2ff; text-align: left;">
                    <th style="padding: 10px;">Sender</th>
                    <th style="padding: 10px;">Receiver</th>
                    <th style="padding: 10px;">Amount</th>
                    <th style="padding: 10px;">Timestamp</th>
                </tr>
            </thead>
            <tbody id="txBody">
                <tr><td colspan="4" style="padding: 15px; text-align: center;">Loading activity...</td></tr>
            </tbody>
        </table>
    </div>

    <script src="../script.js"></script>
    <script>
        function updateVisibilityUI() {
            const isPrivate = localStorage.getItem("balancePrivate") === "true";
            const btn = document.getElementById("visibilityBtn");
            const balEl = document.getElementById("userBalance");

            if (isPrivate) {
                btn.textContent = "🔒 Visibility: Private (Hidden)";
                btn.classList.add("private");
                if (balEl) balEl.textContent = "••••••";
            } else {
                btn.textContent = "👁️ Visibility: Public";
                btn.classList.remove("private");
            }
        }

        function toggleBalanceVisibility() {
            const isPrivate = localStorage.getItem("balancePrivate") === "true";
            localStorage.setItem("balancePrivate", (!isPrivate).toString());
            updateVisibilityUI();
            if (typeof fetchEcosystemData === "function") fetchEcosystemData();
        }

        document.addEventListener("DOMContentLoaded", () => {
            updateVisibilityUI();
        });
    </script>
</body>
</html>'''

with open("html/index.html", "w") as f:
    f.write(dash_html)

print("html/index.html updated with visibility toggle!")
