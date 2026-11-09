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
        <p style="margin-bottom: 20px;">Live, cryptographic chain of mined blocks stored in MySQL database:</p>

        <div id="blocks">
            <div style="text-align: center; padding: 30px; color: #00d2ff; font-weight: bold;">Loading ledger blocks...</div>
        </div>
    </div>

    <script src="../script.js"></script>
    <script>
        async function loadBlockchainLedger() {
            try {
                const res = await fetch("/BitForge/api/blockchain");
                const data = await res.json();
                const container = document.getElementById("blocks");

                if (data.success && data.blocks && container) {
                    if (data.blocks.length === 0) {
                        container.innerHTML = '<div style="text-align: center; padding: 20px;">No blocks mined yet.</div>';
                    } else {
                        container.innerHTML = data.blocks.map(b => `
                            <div style="border: 1px solid #00d2ff; padding: 20px; margin-bottom: 18px; border-radius: 12px; background: rgba(0, 210, 255, 0.04);">
                                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,210,255,0.2); padding-bottom: 10px;">
                                    <strong style="color: #00d2ff; font-size: 1.15rem;">Block #${b.index}</strong>
                                    <span style="background: #27ae60; color: #fff; padding: 4px 12px; border-radius: 5px; font-weight: bold; font-size: 0.8rem;">● Validated Hash</span>
                                </div>
                                <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 12px;"><strong>Previous Hash:</strong> <span style="font-family: monospace;">${b.prev}</span></div>
                                <div style="font-family: monospace; color: #00d2ff; margin: 8px 0; word-break: break-all;"><strong>Current Block Hash:</strong> ${b.hash}</div>
                                <div style="margin-top: 8px;"><span>Payload / Transaction Data: </span><strong style="color: #2ecc71;">${b.data}</strong></div>
                                <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 10px;">Nonce: ${b.nonce} | Mined Timestamp: ${b.time}</div>
                            </div>
                        `).join("");
                    }
                }
            } catch (err) {}
        }

        document.addEventListener("DOMContentLoaded", () => {
            loadBlockchainLedger();
            setInterval(loadBlockchainLedger, 3000);
        });
    </script>
</body>
</html>'''

with open("html/blockchain.html", "w") as f:
    f.write(bc_html)

print("html/blockchain.html updated!")
