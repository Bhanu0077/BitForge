net_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Network Peers</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .node-card { border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
        .status-online { color: #2ecc71; font-weight: bold; }
    </style>
</head>
<body>
    <nav>
        <a href="index.html">Dashboard</a>
        <a href="wallet.html">Wallet</a>
        <a href="transactions.html">Transactions / Pay</a>
        <a href="mining.html">Mining</a>
        <a href="blockchain.html">Ledger</a>
        <a href="network.html" class="active">Network</a>
        <button onclick="logout()" style="background: #e74c3c; padding: 5px 15px; border: none; cursor: pointer;">Logout</button>
    </nav>

    <div class="container" style="padding: 20px;">
        <h2>Active P2P Network Nodes</h2>
        <p>Live Tomcat consensus nodes broadcasting block data:</p>

        <div style="margin-top: 20px;">
            <div class="node-card">
                <div>
                    <strong>Node #1 (Local Primary Tomcat Engine)</strong>
                    <div style="font-size: 0.85rem; opacity: 0.7;">IP: 127.0.0.1:8080 | Protocol: Jakarta Servlet 6.0</div>
                </div>
                <span class="status-online">● ACTIVE (Leader)</span>
            </div>

            <div class="node-card">
                <div>
                    <strong>Node #2 (MySQL Persistence Storage)</strong>
                    <div style="font-size: 0.85rem; opacity: 0.7;">IP: 127.0.0.1:3306 | Engine: InnoDB Concurrent</div>
                </div>
                <span class="status-online">● CONNECTED</span>
            </div>

            <div class="node-card">
                <div>
                    <strong>Node #3 (Client Peer Web Worker)</strong>
                    <div style="font-size: 0.85rem; opacity: 0.7;">Active User: <span data-user style="color: #00d2ff;">You</span></div>
                </div>
                <span class="status-online">● SYNCED (2s Poll)</span>
            </div>
        </div>
    </div>

    <script src="../script.js"></script>
</body>
</html>'''

with open("html/network.html", "w") as f:
    f.write(net_html)

print("html/network.html updated!")
