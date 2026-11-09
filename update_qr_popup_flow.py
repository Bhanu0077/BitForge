tx_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitForge - Pay & Send Money</title>
    <link rel="stylesheet" href="../style.css">
    <script src="https://unpkg.com/html5-qrcode"></script>
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

        .qr-scanner-wrapper { border: 2px dashed #00d2ff; padding: 20px; text-align: center; border-radius: 12px; background: rgba(0, 210, 255, 0.02); }
        #qr-reader { width: 100%; max-width: 400px; margin: 15px auto; border-radius: 8px; overflow: hidden; }

        /* Modal Overlay Styles */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); justify-content: center; align-items: center; z-index: 1000; }
        .modal-overlay.active { display: flex; }
        .modal-card { background: #1e1e1e; border: 2px solid #00d2ff; padding: 25px; border-radius: 16px; width: 90%; max-width: 420px; box-shadow: 0 0 25px rgba(0,210,255,0.3); }
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

        <div class="pay-card">
            <div>
                <p><strong>Logged in as:</strong> <span data-user style="color: #00d2ff; font-weight: bold;">Loading...</span></p>
                <p><strong>Available Balance:</strong> <span id="userBalance" style="color: #2ecc71; font-size: 1.6rem; font-weight: bold;">0.00</span> BFG</p>
            </div>
            <div>
                <button class="btn-history" onclick="openHistoryModal()">📜 My Transaction History</button>
            </div>
        </div>

        <h3 style="margin-bottom: 5px;">People & Contacts (Select to Pay)</h3>
        <p style="font-size: 0.9rem; opacity: 0.7;">Click any registered user to initiate instant transfer:</p>
        
        <div class="contact-grid" id="peopleGrid">
            <div style="grid-column: 1 / -1; text-align: center; opacity: 0.7;">Loading network contacts...</div>
        </div>

        <!-- Payment Mode Tabs -->
        <div style="display: flex; gap: 10px;">
            <button class="tab-btn active" onclick="switchPayTab('standard', this)">Direct Payment</button>
            <button class="tab-btn" onclick="switchPayTab('qr', this)">📷 Live QR Scan & Pay</button>
        </div>

        <!-- 1. Direct Transfer Form -->
        <div id="tab-standard" class="tab-content active">
            <form onsubmit="sendCoins(event)" style="border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                <label>Receiver Account Email</label>
                <input type="email" id="receiver" required placeholder="Select a contact above or type email..." style="width: 100%; margin-bottom: 15px; padding: 10px;">
                
                <label>Amount to Send (BFG)</label>
                <input type="number" step="0.01" min="0.01" id="amount" required placeholder="10.00" style="width: 100%; margin-bottom: 20px; padding: 10px;">
                
                <button type="submit" style="width: 100%; padding: 14px; background: #00d2ff; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 6px; font-size: 1rem;">⚡ Send BFG Now</button>
            </form>
        </div>

        <!-- 2. Live Webcam Scanner Tab -->
        <div id="tab-qr" class="tab-content">
            <div class="qr-scanner-wrapper">
                <h3>📷 Live Camera QR Scanner</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">Point your webcam at another user's wallet QR code:</p>
                <div id="qr-reader"></div>
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

    <!-- CLEAN QR PAYMENT MODAL -->
    <div class="modal-overlay" id="qrPayModal">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #00d2ff; padding-bottom: 10px; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #00d2ff;">⚡ Complete QR Transfer</h3>
                <button onclick="closeQRPayModal()" style="background: #e74c3c; color: #fff; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; font-weight: bold;">✕ Cancel</button>
            </div>

            <!-- Recipient Username/Email Display -->
            <div style="background: rgba(0,210,255,0.08); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,210,255,0.2); margin-bottom: 20px; text-align: center;">
                <span style="font-size: 0.85rem; opacity: 0.7; display: block; margin-bottom: 4px;">Paying Recipient:</span>
                <strong id="modalTargetUser" style="color: #2ecc71; font-size: 1.15rem; word-break: break-all;">user@example.com</strong>
            </div>

            <!-- Single Amount Field Form -->
            <form onsubmit="submitQRPopupPayment(event)">
                <label style="display: block; margin-bottom: 8px; font-weight: bold;">Amount to Send (BFG):</label>
                <input type="number" step="0.01" min="0.01" id="popupAmount" required placeholder="e.g. 50.00" autofocus style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #00d2ff; background: #0f172a; color: #fff; font-size: 1.1rem; margin-bottom: 20px;">

                <button type="submit" style="width: 100%; padding: 14px; background: #2ecc71; color: #fff; font-weight: bold; border: none; cursor: pointer; border-radius: 6px; font-size: 1.05rem;">⚡ Send BFG</button>
            </form>
        </div>
    </div>

    <!-- Personal History Modal -->
    <div class="modal-overlay" id="historyModal">
        <div class="modal-card" style="max-width: 650px;">
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
        let html5QrcodeScanner = null;
        let scannedTargetEmail = "";

        function switchPayTab(tabId, btn) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');

            if (tabId === 'qr') {
                startQRScanner();
            } else {
                stopQRScanner();
            }
        }

        function startQRScanner() {
            if (!html5QrcodeScanner) {
                html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: 250 });
                html5QrcodeScanner.render((decodedText) => {
                    // 1. Freeze / Pause scanning upon detection
                    if (html5QrcodeScanner) {
                        html5QrcodeScanner.pause(true);
                    }

                    // 2. Extract recipient username/email & display clean popup
                    scannedTargetEmail = decodedText.trim();
                    document.getElementById("modalTargetUser").textContent = scannedTargetEmail;
                    document.getElementById("popupAmount").value = "";
                    document.getElementById("qrPayModal").classList.add("active");
                    
                    // Focus on the amount input automatically
                    setTimeout(() => {
                        document.getElementById("popupAmount").focus();
                    }, 200);

                    *Verification:* The scanner pauses immediately and the payment popup opens displaying the scanned email.
                }, (error) => {});
            }
        }

        function stopQRScanner() {
            if (html5QrcodeScanner) {
                html5QrcodeScanner.clear().catch(error => {});
                html5QrcodeScanner = null;
            }
        }

        function closeQRPayModal() {
            document.getElementById("qrPayModal").classList.remove("active");
            // Unfreeze / Resume camera scanning
            if (html5QrcodeScanner) {
                try {
                    html5QrcodeScanner.resume();
                } catch(e) {}
            }
        }

        function submitQRPopupPayment(event) {
            event.preventDefault();
            const amount = Number(document.getElementById("popupAmount").value);
            
            if (!scannedTargetEmail || amount <= 0) {
                alert("Please enter a valid amount.");
                return;
            }

            // Close popup and execute backend transfer
            closeQRPayModal();
            executePayment(scannedTargetEmail, amount);
        }

        function selectContact(email) {
            document.getElementById("receiver").value = email;
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
print("html/transactions.html updated with clean QR popup & scanner freezing!")
