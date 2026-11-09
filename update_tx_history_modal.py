tx_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Pay & Send Money</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .pay-card { border: 1px solid #00d2ff; padding: 20px; border-radius: 12px; margin-bottom: 20px; background: rgba(0, 210, 255, 0.05); display: flex; justify-content: space-between; align-items: center; }
        .contact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; margin: 15px 0 25px 0; }
        .contact-avatar { display: flex; flex-direction: column; align-items: center; cursor: pointer; padding: 12px; border-radius: 12px; background: #1e1e1e; border: 2px solid transparent; transition: all 0.2s; }
        .contact-avatar:hover, .contact-avatar.selected { border-color: #00d2ff; background: rgba(0, 210, 255, 0.15); transform: translateY(-2px); }
        .avatar-circle { width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #00d2ff, #9b59b6); display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.3rem; color: #fff; margin-bottom: 8px; text-transform: uppercase; }
        .contact-name { font-size: 0.85rem; font-weight: bold; text-align: center; word-break: break-all; opacity: 0.9; }
        .tab-btn { padding: 10px 20px; background: #1e1e1e; color: #fff; border: 1px solid #00d2ff; cursor: pointer; border-radius: 5px; font-weight: bold; }
        .tab-btn.active { background: #00d2ff; color: #000; }
        .tab-content { display: none; margin-top: 15px; }
        .tab-content.active { display: block; }
        
        .btn-history { padding: 12px 24px; background: #8e44ad; color: #fff; font-weight: bold; border: none; cursor: pointer; border-radius: 6px; font-size: 0.95rem; }
        .btn-history:hover { background: #9b59b6; }

        /* Modal Popup Styles */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); justify-content: center; align-items: center; z-index: 1000; }
        .modal-overlay.active { display: flex; }
        .modal-card { background: #1e1e1e; border: 1px solid #00d2ff; padding: 25px; border-radius: 12px; width: 90%; max-width: 650px; max-height: 80vh; overflow-y: auto; box-shadow: 0 0 20px rgba(0,210,255,0.3); }
    </style>
</head>
<body>
    <nav>
        <a href="index.html">Dashboard</a>
        <a href="wallet.html">Wallet</a>
        <a href="transactions.html" class="active">Transactions / Pay</a>
        <a href="mining.html">Mining</a>
        <a href="blockchain.html">Ledger</a>
        <a href="network.html">Network</a>
        <button onclick="logout()" style="background: #e74c3c; padding: 5px 15px; border: none; cursor: pointer;">Logout</button>
    </nav>

    <div class="container" style="padding: 20px;">
        <h2>Send & Receive Money</h2>

        <!-- Active Wallet Banner with History Popup Button -->
        <div class="pay-card">
            <div>
                <p><strong>Logged in as:</strong> <span data-user style="color: #00d2ff; font-weight: bold;">Loading...</span></p>
                <p><strong>Available Balance:</strong> <span id="userBalance" style="color: #2ecc71; font-size: 1.6rem; font-weight: bold;">0.00</span> BFG</p>
            </div>
            <div>
                <button class="btn-history" onclick="openHistoryModal()">📜 My Transaction History</button>
            </div>
        </div>

        <!-- Google Pay / PhonePe Style People Grid -->
        <h3 style="margin-bottom: 5px;">People & Contacts (Select to Pay)</h3>
        <p style="font-size: 0.9rem; opacity: 0.7;">Click any registered user to initiate instant transfer:</p>
        
        <div class="contact-grid" id="peopleGrid">
            <div style="grid-column: 1 / -1; text-align: center; opacity: 0.7;">Loading network contacts...</div>
        </div>

        <!-- Payment Mode Tabs -->
        <div style="display: flex; gap: 10px;">
            <button class="tab-btn active" onclick="switchPayTab('standard', this)">Direct Payment</button>
            <button class="tab-btn" onclick="switchPayTab('qr', this)">QR Scan & Pay</button>
            <button class="tab-btn" onclick="switchPayTab('nfc', this)">NFC Tap-to-Pay</button>
        </div>

        <!-- Direct Transfer Form -->
        <div id="tab-standard" class="tab-content active">
            <form onsubmit="sendCoins(event)" style="border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                <label>Receiver Account Email</label>
                <input type="email" id="receiver" required placeholder="Select a contact above or type email..." style="width: 100%; margin-bottom: 15px; padding: 10px;">
                
                <label>Amount to Send (BFG)</label>
                <input type="number" step="0.01" min="0.01" id="amount" required placeholder="10.00" style="width: 100%; margin-bottom: 20px; padding: 10px;">
                
                <button type="submit" style="width: 100%; padding: 14px; background: #00d2ff; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 6px; font-size: 1rem;">⚡ Send BFG Now</button>
            </form>
        </div>

        <!-- QR Code Scanner -->
        <div id="tab-qr" class="tab-content">
            <div style="border: 2px dashed #00d2ff; padding: 30px; text-align: center; border-radius: 8px;">
                <h3>WebCam QR Code Payment</h3>
                <p>Scan recipient's wallet QR or select from people grid above.</p>
                <div style="margin-top: 15px;">
                    <input type="email" id="qrTarget" placeholder="Target Email" style="padding: 10px; width: 60%;">
                    <input type="number" id="qrAmount" placeholder="Amount" value="25.00" style="padding: 10px; width: 30%;">
                </div>
                <button onclick="triggerQRTransfer()" style="margin-top: 15px; padding: 12px 25px; background: #27ae60; color: #fff; font-weight: bold; border: none; cursor: pointer; border-radius: 5px;">[Simulate Camera Scan & Pay]</button>
            </div>
        </div>

        <!-- NFC Tap-to-Pay -->
        <div id="tab-nfc" class="tab-content">
            <div style="border: 2px solid #9b59b6; padding: 30px; text-align: center; border-radius: 12px; background: rgba(155, 89, 182, 0.05);">
                <span style="font-size: 3.5rem;">📱⚡📱</span>
                <h3>Web NFC Contactless Tap</h3>
                <div style="margin-top: 15px;">
                    <input type="email" id="nfcTarget" placeholder="Target Email" style="padding: 10px; width: 60%;">
                    <input type="number" id="nfcAmount" placeholder="Amount" value="50.00" style="padding: 10px; width: 30%;">
                </div>
                <button onclick="triggerNFCTransfer()" style="margin-top: 15px; padding: 12px 25px; background: #8e44ad; color: #fff; font-weight: bold; border: none; cursor: pointer; border-radius: 5px;">Execute Instant Device Tap</button>
            </div>
        </div>

        <div id="message" class="message" style="margin-top: 20px; font-weight: bold; text-align: center;"></div>

        <h3 style="margin-top: 35px;">Live Network Ledger</h3>
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
                <tr><td colspan="4" style="padding: 15px; text-align: center;">Loading ledger activity...</td></tr>
            </tbody>
        </table>
    </div>

    <!-- Personal History Modal -->
    <div class="modal-overlay" id="historyModal">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #00d2ff; padding-bottom: 10px;">
                <h3 style="margin: 0; color: #00d2ff;">📜 My Personal Transaction History</h3>
                <button onclick="closeHistoryModal()" style="background: #e74c3c; color: #fff; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; font-weight: bold;">✕ Close</button>
            </div>

            <table style="width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.9rem;">
                <thead>
                    <tr style="border-bottom: 1px solid #00d2ff; text-align: left;">
                        <th style="padding: 8px;">Type</th>
                        <th style="padding: 8px;">Counterparty</th>
                        <th style="padding: 8px;">Amount</th>
                        <th style="padding: 8px;">Time</th>
                    </tr>
                </thead>
                <tbody id="historyModalBody">
                    <tr><td colspan="4" style="padding: 10px; text-align: center;">Loading your history...</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <script src="../script.js"></script>
    <script>
        function switchPayTab(tabId, btn) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');
        }

        function selectContact(email) {
            document.getElementById("receiver").value = email;
            document.getElementById("qrTarget").value = email;
            document.getElementById("nfcTarget").value = email;
            document.querySelectorAll('.contact-avatar').forEach(c => c.classList.remove('selected'));
            event.currentTarget.classList.add('selected');
        }

        async function openHistoryModal() {
            const user = localStorage.getItem("bitforgeUser") || "bhanu@gmail.com";
            document.getElementById("historyModal").classList.add("active");
            
            try {
                const res = await fetch("/BitForge/api/transactions");
                const data = await res.json();
                const historyBody = document.getElementById("historyModalBody");
                
                if (data.transactions) {
                    const myTxs = data.transactions.filter(t => 
                        t.from.toLowerCase() === user.toLowerCase() || t.to.toLowerCase() === user.toLowerCase()
                    );

                    if (myTxs.length === 0) {
                        historyBody.innerHTML = '<tr><td colspan="4" style="padding: 15px; text-align: center;">No transaction history found for your account.</td></tr>';
                    } else {
                        historyBody.innerHTML = myTxs.map(t => {
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

        function closeHistoryModal() {
            document.getElementById("historyModal").classList.remove("active");
        }
    </script>
</body>
</html>'''

with open("html/transactions.html", "w") as f:
    f.write(tx_html)
print("html/transactions.html updated with history modal!")
