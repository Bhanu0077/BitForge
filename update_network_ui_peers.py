net_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Network Peers & User Directory</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }
        .net-card { border: 1px solid #00d2ff; padding: 20px; border-radius: 10px; background: rgba(0, 210, 255, 0.05); }
        .peer-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; margin-top: 20px; }
        .peer-card { border: 1px solid rgba(0, 210, 255, 0.3); padding: 18px; border-radius: 10px; background: #1a1a1a; display: flex; justify-content: space-between; align-items: center; }
        .peer-avatar { width: 45px; height: 45px; border-radius: 50%; background: linear-gradient(135deg, #00d2ff, #2ecc71); display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; color: #000; text-transform: uppercase; }
        .pay-peer-btn { padding: 8px 15px; background: #00d2ff; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; text-decoration: none; font-size: 0.85rem; }
        .pay-peer-btn:hover { background: #2ecc71; color: #fff; }
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
        <h2>Network Users & Public Ledger Inspection</h2>
        <p>Inspect public wallet balances across active users in the BitForge network and initiate instant payments:</p>

        <!-- Network Quick Telemetry -->
        <div class="grid-3">
            <div class="net-card">
                <h4 style="opacity: 0.8; margin: 0;">Total Ecosystem Peers</h4>
                <h1 id="netUsers" style="color: #00d2ff; margin: 10px 0;">--</h1>
            </div>
            <div class="net-card">
                <h4 style="opacity: 0.8; margin: 0;">Mined Chain Blocks</h4>
                <h1 id="netBlocks" style="color: #2ecc71; margin: 10px 0;">--</h1>
            </div>
            <div class="net-card">
                <h4 style="opacity: 0.8; margin: 0;">Total Network Transactions</h4>
                <h1 id="netTxs" style="color: #9b59b6; margin: 10px 0;">--</h1>
            </div>
        </div>

        <h3 style="margin-top: 35px;">Active Peer User Directory</h3>
        <div class="peer-grid" id="peerDirectory">
            <div style="grid-column: 1 / -1; text-align: center; opacity: 0.7;">Loading network peers...</div>
        </div>
    </div>

    <script src="../script.js"></script>
    <script>
        async function loadPeersDirectory() {
            try {
                const res = await fetch("/BitForge/api/network");
                const data = await res.json();
                if (data.success) {
                    document.getElementById("netUsers").textContent = data.users;
                    document.getElementById("netBlocks").textContent = data.blocks;
                    document.getElementById("netTxs").textContent = data.transactions;

                    const activeUser = localStorage.getItem("bitforgeUser") || "";
                    const peerGrid = document.getElementById("peerDirectory");

                    if (data.peers && data.peers.length > 0) {
                        peerGrid.innerHTML = data.peers.map(p => {
                            const initial = p.email.charAt(0).toUpperCase();
                            const isSelf = p.email.toLowerCase() === activeUser.toLowerCase();
                            
                            return `
                                <div class="peer-card" style="${isSelf ? 'border-color: #2ecc71;' : ''}">
                                    <div style="display: flex; align-items: center; gap: 12px;">
                                        <div class="peer-avatar">${initial}</div>
                                        <div>
                                            <strong style="font-size: 0.95rem;">${p.email}</strong> ${isSelf ? '<span style="color: #2ecc71; font-size: 0.75rem;">(You)</span>' : ''}
                                            <div style="font-size: 0.85rem; color: #2ecc71; font-weight: bold; margin-top: 3px;">
                                                Balance: ${p.balance.toFixed(2)} BFG
                                            </div>
                                        </div>
                                    </div>
                                    <div>
                                        ${!isSelf ? `<button class="pay-peer-btn" onclick="payTargetUser('${p.email}')">⚡ Send BFG</button>` : '<span style="opacity: 0.5; font-size: 0.8rem;">Owner</span>'}
                                    </div>
                                </div>
                            `;
                        }).join("");
                    } else {
                        peerGrid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center;">No peer users found.</div>';
                    }
                }
            } catch (err) {}
        }

        function payTargetUser(email) {
            localStorage.setItem("selectedPayTarget", email);
            window.location.href = "transactions.html";
        }

        document.addEventListener("DOMContentLoaded", () => {
            loadPeersDirectory();
            setInterval(loadPeersDirectory, 3000);
        });
    </script>
</body>
</html>'''

with open("html/network.html", "w") as f:
    f.write(net_html)
print("html/network.html updated with direct peer selection!")
