bc_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Blockchain Explorer</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <nav>
        <a href="index.html">Dashboard</a>
        <a href="wallet.html">Wallet</a>
        <a href="transactions.html">Transactions / Pay</a>
        <a href="mining.html">Mining</a>
        <a href="blockchain.html" class="active">Ledger</a>
        <a href="network.html">Network</a>
        <button onclick="logout()" style="background: #e74c3c; padding: 5px 15px; border: none; cursor: pointer;">Logout</button>
    </nav>

    <div class="container" style="padding: 20px;">
        <h2>Immutable Blockchain Ledger Explorer</h2>
        <p>Live, cryptographic chain of mined blocks stored in MySQL database:</p>

        <div id="blocks" style="margin-top: 25px;">
            <p style="text-align: center;">Loading ledger blocks...</p>
        </div>
    </div>

    <script src="../script.js"></script>
</body>
</html>'''

with open("html/blockchain.html", "w") as f:
    f.write(bc_html)
print("html/blockchain.html updated!")
