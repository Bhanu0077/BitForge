mining_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Mining Engine</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .mining-card { border: 1px solid #00d2ff; padding: 25px; border-radius: 10px; background: rgba(0, 210, 255, 0.05); text-align: center; margin-bottom: 20px; }
        .hash-display { font-family: monospace; font-size: 1.1rem; color: #00d2ff; word-break: break-all; margin: 15px 0; padding: 10px; background: #1e1e1e; border-radius: 5px; }
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
        <h2>BitForge Proof-of-Work Engine</h2>

        <div class="mining-card">
            <h3>Active Mining Node</h3>
            <p><strong>Miner Identity:</strong> <span data-user style="color: #00d2ff;">Loading...</span></p>
            <p><strong>Block Reward:</strong> <span style="color: #2ecc71; font-weight: bold;">+10.00 BFG</span></p>

            <div style="margin: 20px 0;">
                <div>Current Nonce calculation: <strong id="nonceVal">0</strong></div>
                <div class="hash-display" id="computedHash">0000000000000000000000000000000000000000000000000000000000000000</div>
            </div>

            <button id="mineBtn" onclick="startProofOfWork()" style="padding: 14px 30px; font-size: 1.1rem; background: #27ae60; color: #fff; font-weight: bold; border: none; cursor: pointer; border-radius: 5px;">⚡ Start Mining Block</button>
        </div>

        <div id="message" class="message" style="margin-top: 20px; font-weight: bold; text-align: center;"></div>
    </div>

    <script src="../script.js"></script>
    <script>
        async function startProofOfWork() {
            const btn = document.getElementById("mineBtn");
            const nonceEl = document.getElementById("nonceVal");
            const hashEl = document.getElementById("computedHash");
            const msg = document.getElementById("message");

            btn.disabled = true;
            btn.textContent = "⚙️ Mining Block (Computing SHA-256 Nonces)...";
            msg.textContent = "";

            let nonce = 0;
            const targetPrefix = "0000";

            // Simulated browser PoW hash computation loop
            const timer = setInterval(() => {
                nonce += Math.floor(Math.random() * 500) + 1;
                nonceEl.textContent = nonce;
                const fakeHash = targetPrefix + Array.from({length: 60}, () => Math.floor(Math.random()*16).toString(16)).join("");
                hashEl.textContent = fakeHash;
            }, 50);

            setTimeout(async () => {
                clearInterval(timer);
                const user = localStorage.getItem("bitforgeUser") || "bhanu@gmail.com";

                try {
                    const res = await fetch("/BitForge/api/mine", {
                        method: "POST",
                        headers: { "Content-Type": "application/x-www-form-urlencoded" },
                        body: `miner=${encodeURIComponent(user)}`
                    });
                    const data = await res.json();
                    if (data.success) {
                        msg.style.color = "#2ecc71";
                        msg.textContent = `🎉 ${data.message} Reward added to your account!`;
                    } else {
                        msg.style.color = "#e74c3c";
                        msg.textContent = data.message;
                    }
                } catch (err) {
                    msg.style.color = "#e74c3c";
                    msg.textContent = "Mining server error.";
                }

                btn.disabled = false;
                btn.textContent = "⚡ Start Mining Block";
            }, 2500);
        }
    </script>
</body>
</html>'''

with open("html/mining.html", "w") as f:
    f.write(mining_html)
print("html/mining.html updated!")
