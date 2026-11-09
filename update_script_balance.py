script_js = '''const API_URL = "/BitForge/api";
const currentUser = localStorage.getItem("bitforgeUser") || "bhanu@gmail.com";

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-user]").forEach(el => {
        el.textContent = currentUser;
    });
    
    fetchEcosystemData();
    setInterval(fetchEcosystemData, 2000);
});

function logout() {
    localStorage.removeItem("bitforgeUser");
    window.location.href = "login.html";
}

function showMessage(text, isError = false) {
    const box = document.getElementById("message") || document.getElementById("authMessage");
    if (box) {
        box.textContent = text;
        box.style.color = isError ? "#e74c3c" : "#2ecc71";
    }
}

// 1. Authentication Handlers
async function handleSignup(event) {
    event.preventDefault();
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value;
    const confirm = document.getElementById("signupConfirm").value;
    const question = document.getElementById("secretQuestion").value;
    const answer = document.getElementById("secretAnswer").value;

    if (password !== confirm) {
        showMessage("Passwords do not match!", true);
        return;
    }

    const payload = `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&question=${encodeURIComponent(question)}&answer=${encodeURIComponent(answer)}`;
    
    try {
        const res = await fetch(`${API_URL}/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();
        
        if (data.success) {
            showMessage("Account created! Initial wallet loaded with 100 BFG. Redirecting...");
            setTimeout(() => window.location.href = "login.html", 1500);
        } else {
            showMessage(data.message, true);
        }
    } catch (err) {
        showMessage("Tomcat backend connection error.", true);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    const payload = `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`;

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();

        if (data.success) {
            localStorage.setItem("bitforgeUser", data.email);
            window.location.href = "index.html";
        } else {
            showMessage(data.message, true);
        }
    } catch (err) {
        showMessage("Login request failed.", true);
    }
}

async function handleForgotPassword(event) {
    event.preventDefault();
    const email = document.getElementById("forgotEmail").value.trim();
    const answer = document.getElementById("forgotAnswer").value;
    const newPassword = document.getElementById("forgotNewPassword").value;

    const payload = `email=${encodeURIComponent(email)}&answer=${encodeURIComponent(answer)}&new_password=${encodeURIComponent(newPassword)}`;

    try {
        const res = await fetch(`${API_URL}/auth/forgot-password`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();
        showMessage(data.message, !data.success);
    } catch (err) {
        showMessage("Password recovery failed.", true);
    }
}

// 2. Synchronous Payment Processor
async function executePayment(receiver, amount) {
    if (!receiver || amount <= 0) {
        showMessage("Please enter a valid receiver email and positive amount.", true);
        return;
    }

    if (receiver.toLowerCase() === currentUser.toLowerCase()) {
        showMessage("You cannot send coins to yourself!", true);
        return;
    }

    const payload = `sender=${encodeURIComponent(currentUser)}&receiver=${encodeURIComponent(receiver)}&amount=${amount}`;

    try {
        const res = await fetch(`${API_URL}/transactions`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();
        showMessage(data.message, !data.success);
        fetchEcosystemData();
    } catch (err) {
        showMessage("Transaction failed to process.", true);
    }
}

function sendCoins(event) {
    event.preventDefault();
    const receiver = document.getElementById("receiver").value.trim();
    const amount = Number(document.getElementById("amount").value);
    executePayment(receiver, amount);
}

function triggerQRTransfer() {
    const target = document.getElementById("qrTarget").value.trim();
    const amount = Number(document.getElementById("qrAmount").value);
    showMessage(`[QR Scanner] Transferring ${amount} BFG to ${target}...`);
    executePayment(target, amount);
}

function triggerNFCTransfer() {
    const target = document.getElementById("nfcTarget").value.trim();
    const amount = Number(document.getElementById("nfcAmount").value);
    showMessage(`[Web NFC] Device contact established. Transferring ${amount} BFG to ${target}...`);
    executePayment(target, amount);
}

// 3. Ecosystem Sync Engine
async function fetchEcosystemData() {
    try {
        const res = await fetch(`${API_URL}/transactions`);
        const data = await res.json();

        // Update Live Transactions Table
        const txBody = document.getElementById("txBody");
        if (txBody && data.transactions) {
            if (data.transactions.length === 0) {
                txBody.innerHTML = '<tr><td colspan="4" style="padding: 15px; text-align: center;">No transactions recorded in the network yet.</td></tr>';
            } else {
                txBody.innerHTML = data.transactions.map(t =>
                    `<tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                        <td style="padding: 10px;"><strong>${t.from}</strong></td>
                        <td style="padding: 10px;">${t.to}</td>
                        <td style="padding: 10px; color: #00d2ff; font-weight: bold;">${t.amount} BFG</td>
                        <td style="padding: 10px; opacity: 0.7;">${t.time}</td>
                    </tr>`
                ).join("");
            }
        }

        // Calculate Live User Balance (Includes Initial 100 BFG + Mined Rewards + Transfers)
        if (data.transactions) {
            let balance = 100.0;
            data.transactions.forEach(t => {
                if (t.to.toLowerCase() === currentUser.toLowerCase()) balance += t.amount;
                if (t.from.toLowerCase() === currentUser.toLowerCase()) balance -= t.amount;
            });
            const balEl = document.getElementById("userBalance");
            if (balEl) balEl.textContent = balance.toFixed(2);
        }

        // Update Blockchain Explorer Ledger
        const blockContainer = document.getElementById("blocks");
        if (blockContainer && data.blocks) {
            document.querySelectorAll("[data-blocks]").forEach(el => el.textContent = data.blocks.length);
            blockContainer.innerHTML = data.blocks.map(b =>
                `<div class="block" style="border: 1px solid #00d2ff; padding: 15px; margin-bottom: 15px; border-radius: 8px;">
                    <div class="block-head" style="display: flex; justify-content: space-between;">
                        <strong>Block #${b.index}</strong>
                        <span class="badge" style="background: #27ae60; padding: 3px 8px; border-radius: 4px;">Valid</span>
                    </div>
                    <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">Previous Hash: ${b.prev.substring(0, 28)}...</div>
                    <div style="font-family: monospace; color: #00d2ff; margin: 5px 0;">Hash: ${b.hash}</div>
                    <div><span>Data: </span><strong>${b.data}</strong></div>
                    <div style="font-size: 0.8rem; opacity: 0.7;">Timestamp: ${b.time}</div>
                </div>`
            ).join("");
        }
    } catch (err) {
    }
}
'''

with open("script.js", "w") as f:
    f.write(script_js)

print("script.js updated!")
