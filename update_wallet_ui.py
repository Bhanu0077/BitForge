wallet_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - My Wallet</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .wallet-card { border: 1px solid #00d2ff; padding: 25px; border-radius: 12px; background: rgba(0, 210, 255, 0.05); }
        .toggle-btn { padding: 8px 16px; background: #34495e; color: #fff; border: 1px solid #00d2ff; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 0.9rem; margin-top: 10px; }
        .toggle-btn.private { background: #e74c3c; border-color: #e74c3c; }
        .action-link { display: inline-block; padding: 10px 20px; background: #00d2ff; color: #000; font-weight: bold; text-decoration: none; border-radius: 5px; margin-top: 12px; }
    </style>
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
        <h2>My BitForge Wallet Dashboard</h2>
        <p>Wallet Address / Identity: <strong data-user style="color: #00d2ff;">Loading...</strong></p>

        <div class="grid-2">
            <!-- Balance & Status Card -->
            <div class="wallet-card">
                <h4 style="opacity: 0.8; margin: 0;">Total Balance</h4>
                <h1 style="color: #2ecc71; margin: 15px 0;"><span id="userBalance">0.00</span> BFG</h1>
                
                <div>
                    <strong>Privacy Setting:</strong>
                    <button id="visibilityBtn" class="toggle-btn" onclick="window.toggleBalanceVisibility()">👁️ Visibility: Public</button>
                </div>

                <div style="margin-top: 20px;">
                    <a href="transactions.html" class="action-link">⚡ Quick Transfer</a>
                    <a href="mining.html" class="action-link" style="background: #27ae60; color: #fff; margin-left: 8px;">⚡ Mine BFG</a>
                </div>
            </div>

            <!-- Wallet Security & Account Overview Card -->
            <div class="wallet-card" style="border-color: #9b59b6; background: rgba(155, 89, 182, 0.05);">
                <h4 style="opacity: 0.8; margin: 0;">Account Information</h4>
                <p style="margin-top: 15px;"><strong>Network Status:</strong> <span style="color: #2ecc71; font-weight: bold;">● Active Peer</span></p>
                <p><strong>Storage Engine:</strong> MySQL 8.3 (`bitforge_db` schema)</p>
                <p><strong>Consensus Layer:</strong> SHA-256 Proof-of-Work</p>
            </div>
        </div>

        <h3 style="margin-top: 35px;">My Personal Wallet Transactions</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
            <thead>
                <tr style="border-bottom: 2px solid #00d2ff; text-align: left;">
                    <th style="padding: 10px;">Type</th>
                    <th style="padding: 10px;">Counterparty</th>
                    <th style="padding: 10px;">Amount</th>
                    <th style="padding: 10px;">Timestamp</th>
                </tr>
            </thead>
            <tbody id="walletTxBody">
                <tr><td colspan="4" style="padding: 15px; text-align: center;">Loading wallet entries...</td></tr>
            </tbody>
        </table>
    </div>

    <script src="../script.js"></script>
    <script>
        async function loadWalletTransactions() {
            const user = localStorage.getItem("bitforgeUser") || "bhanu@gmail.com";
            try {
                const res = await fetch("/BitForge/api/transactions");
                const data = await res.json();
                const body = document.getElementById("walletTxBody");

                if (data.transactions && body) {
                    const myTxs = data.transactions.filter(t => 
                        t.from.toLowerCase() === user.toLowerCase() || t.to.toLowerCase() === user.toLowerCase()
                    );

                    if (myTxs.length === 0) {
                        body.innerHTML = '<tr><td colspan="4" style="padding: 15px; text-align: center;">No activity recorded for this wallet yet.</td></tr>';
                    } else {
                        body.innerHTML = myTxs.map(t => {
                            const isSent = t.from.toLowerCase() === user.toLowerCase();
                            const typeBadge = isSent ? '<span style="color:#e74c3c; font-weight:bold;">SENT</span>' : '<span style="color:#2ecc71; font-weight:bold;">RECEIVED</span>';
                            const party = isSent ? t.to : t.from;
                            return `
                                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                                    <td style="padding: 10px;">${typeBadge}</td>
                                    <td style="padding: 10px;">${party}</td>
                                    <td style="padding: 10px; font-weight: bold; color: ${isSent ? '#e74c3c' : '#2ecc71'};">${isSent ? '-' : '+'}${t.amount} BFG</td>
                                    <td style="padding: 10px; opacity: 0.7;">${t.time}</td>
                                </tr>
                            `;
                        }).join("");
                    }
                }
            } catch (err) {}
        }

        document.addEventListener("DOMContentLoaded", () => {
            loadWalletTransactions();
            setInterval(loadWalletTransactions, 3000);
        });
    </script>
</body>
</html>'''

with open("html/wallet.html", "w") as f:
    f.write(wallet_html)
print("html/wallet.html updated!")
