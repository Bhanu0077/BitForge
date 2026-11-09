index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Dashboard</title>
    <link rel="stylesheet" href="../style.css">
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
        <h2>Welcome to BitForge, <span data-user style="color: #00d2ff;">Loading...</span></h2>
        
        <div style="display: flex; gap: 20px; margin-top: 20px;">
            <div style="flex: 1; border: 1px solid #00d2ff; padding: 20px; border-radius: 8px;">
                <h3>Total Ecosystem Blocks</h3>
                <h1 data-blocks style="color: #00d2ff; font-size: 2.5rem;">1</h1>
            </div>
            <div style="flex: 1; border: 1px solid #2ecc71; padding: 20px; border-radius: 8px;">
                <h3>Active Network Engine</h3>
                <h1 style="color: #2ecc71; font-size: 2.5rem;">Tomcat 11</h1>
            </div>
        </div>

        <div id="message" class="message" style="margin-top: 20px;"></div>
    </div>

    <script src="../script.js"></script>
</body>
</html>'''

wallet_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Wallet</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <nav>
        <a href="index.html">Dashboard</a>
        <a href="wallet.html" class="active">Wallet</a>
        <a href="transactions.html">Transactions / Pay</a>
        <a href="mining.html">Mining</a>
        <a href="blockchain.html">Ledger</a>
        <a href="network.html">Network</a>
        <button onclick="logout()" style="background: #e74c3c; padding: 5px 15px; border: none; cursor: pointer;">Logout</button>
    </nav>

    <div class="container" style="padding: 20px;">
        <h2>Your BitForge Wallet</h2>
        <div style="border: 1px solid #00d2ff; padding: 25px; border-radius: 10px; margin-top: 20px;">
            <p><strong>Account Email:</strong> <span data-user style="color: #00d2ff;">Loading...</span></p>
            <p><strong>Ecosystem Role:</strong> Active Node / Miner</p>
            <p><strong>Status:</strong> <span style="color: #2ecc71;">Synchronized with Database</span></p>
        </div>
    </div>

    <script src="../script.js"></script>
</body>
</html>'''

with open("html/index.html", "w") as f:
    f.write(index_html)
with open("html/wallet.html", "w") as f:
    f.write(wallet_html)

print("html/index.html and html/wallet.html updated!")
