mining_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Mining Engine</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .mine-card { border: 1px solid #00d2ff; padding: 30px; border-radius: 12px; background: rgba(0, 210, 255, 0.05); text-align: center; max-width: 600px; margin: 30px auto; }
        .hash-display { font-family: monospace; font-size: 1.1rem; color: #00d2ff; background: #0f172a; padding: 15px; border-radius: 8px; word-break: break-all; margin: 20px 0; border: 1px solid rgba(0,210,255,0.2); }
        .btn-mine { padding: 15px 35px; background: #27ae60; color: #fff; font-size: 1.2rem; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
        .btn-mine:hover { background: #2ecc71; transform: scale(1.02); }
        .btn-mine:disabled { background: #7f8c8d; cursor: not-allowed; }
    </style>
</head>
<body>
    <nav>
        <a href="index.html">Dashboard</a>
        <a href="wallet.html">Wallet</a>
        <a href="transactions.html">Transactions / Pay</a>
        <a href="mining.html" class="active">Mining</a>
        <a href="blockchain.html">Ledger</a>
        <a href="network.html">Network</a>
        <button onclick="logout()" style="background: #e74c3c; padding: 5px 15px; border: none; cursor: pointer;">Logout</button>
    </nav>

    <div class="container" style="padding: 20px;">
        <h2 style="text-align: center;">BitForge Proof-of-Work Engine</h2>

        <div class="mine-card">
            <h3>Active Mining Node</h3>
            <p style="margin-top: 8px;">Miner Identity: <strong data-user style="color: #00d2ff;">Loading...</strong></p>
            <p style="margin-top: 4px;">Block Reward: <strong style="color: #2ecc71;">+10.00 BFG</strong></p>

            <div style="margin-top: 20px;" id="nonceBox">Current Nonce calculation: <span id="nonceVal">11010</span></div>

            <div class="hash-display" id="hashDisplay">
                00003447af942de333d71083107008ea4740124e4f70aa15b03a3c6889388988
            </div>

            <button class="btn-mine" id="mineBtn" onclick="executeProofOfWork()">⚡ Start Mining Block</button>

            <div id="message" style="margin-top: 20px; font-weight: bold;"></div>
        </div>
    </div>

    <script src="../script.js"></script>
    <script>
        async function executeProofOfWork() {
            const user = localStorage.getItem("bitforgeUser") || "test";
            const btn = document.getElementById("mineBtn");
            const hashBox = document.getElementById("hashDisplay");
            const nonceBox = document.getElementById("nonceVal");
            const msg = document.getElementById("message");

            btn.disabled = true;
            btn.textContent = "⏳ Calculating Proof-of-Work...";
            msg.textContent = "";

            let iterations = 0;
            const interval = setInterval(() => {
                const randomNonce = Math.floor(Math.random() * 90000) + 10000;
                const fakeHash = "0000" + Array.from({length: 60}, () => Math.floor(Math.random()*16).toString(16)).join("");
                nonceBox.textContent = randomNonce;
                hashBox.textContent = fakeHash;
                iterations++;

                if (iterations >= 15) {
                    clearInterval(interval);
                    submitMinedBlock(user);
                }
            }, 100);
        }

        async function submitMinedBlock(user) {
            const btn = document.getElementById("mineBtn");
            try {
                const res = await fetch("/BitForge/api/mining", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: `username=${encodeURIComponent(user)}&reward=10.0`
                });
                const data = await res.json();

                if (data.success) {
                    document.getElementById("hashDisplay").textContent = data.hash;
                    document.getElementById("nonceVal").textContent = data.nonce;
                    showMessage("✅ " + data.message, false);
                    if (typeof showToast === "function") {
                        showToast("⛏️ Block successfully mined! +10.00 BFG added to balance.", "success");
                    }
                } else {
                    showMessage("⚠️ " + data.message, true);
                }
            } catch (err) {
                showMessage("⚠️ Connection to mining server failed.", true);
            } finally {
                btn.disabled = false;
                btn.textContent = "⚡ Start Mining Block";
            }
        }
    </script>
</body>
</html>'''

with open("html/mining.html", "w") as f:
    f.write(mining_html)

print("html/mining.html updated!")
