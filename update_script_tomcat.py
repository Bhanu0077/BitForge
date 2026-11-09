script_js = '''const API_URL = "/BitForge/api";
const currentUser = localStorage.getItem("bitforgeUser") || "bhanu@bitforge.org";

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-user]").forEach(el => {
        el.textContent = currentUser;
    });
    
    // Periodically fetch synchronous data (every 3 seconds) across multi-user ecosystem
    fetchEcosystemData();
    setInterval(fetchEcosystemData, 3000);
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

// 1. Authentication Handlers (Goal 1)
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
            showMessage("Signup successful! Redirecting to login...");
            setTimeout(() => window.location.href = "login.html", 1500);
        } else {
            showMessage(data.message, true);
        }
    } catch (err) {
        showMessage("Tomcat Servlet connection error.", true);
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
        showMessage("Tomcat authentication failed.", true);
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
        showMessage("Password reset request failed.", true);
    }
}

// 2. Seamless Transactions (Goals 2 & 3: Standard, QR Scan & NFC Tap)
async function executePayment(receiver, amount) {
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
        showMessage("Transaction processing failed.", true);
    }
}

function sendCoins(event) {
    event.preventDefault();
    const receiver = document.getElementById("receiver").value.trim();
    const amount = Number(document.getElementById("amount").value);
    executePayment(receiver, amount);
}

function simulateQRScan(receiver, amount) {
    showMessage(`QR Code Scanned! Transferring ${amount} BFG to ${receiver}...`);
    executePayment(receiver, amount);
}

function triggerNFCTap(receiver, amount) {
    showMessage(`NFC Contactless Tap Detected! Transferring ${amount} BFG to ${receiver}...`);
    executePayment(receiver, amount);
}

// 3. Mining Engine (Goal 2)
async function addBlock() {
    const payload = `miner=${encodeURIComponent(currentUser)}`;
    try {
        const res = await fetch(`${API_URL}/mine`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();
        showMessage(data.message, !data.success);
        fetchEcosystemData();
    } catch (err) {
        showMessage("Mining request failed.", true);
    }
}

// 4. Synchronous Ecosystem Sync (Goal 2)
async function fetchEcosystemData() {
    try {
        const res = await fetch(`${API_URL}/transactions`);
        const data = await res.json();

        // Update Live Transactions Table
        const txBody = document.getElementById("txBody");
        if (txBody && data.transactions) {
            if (data.transactions.length === 0) {
                txBody.innerHTML = '<tr><td colspan="4">No transactions recorded yet.</td></tr>';
            } else {
                txBody.innerHTML = data.transactions.map(t =>
                    `<tr>
                        <td><strong>${t.from}</strong></td>
                        <td>${t.to}</td>
                        <td>${t.amount} BFG</td>
                        <td>${t.time}</td>
                    </tr>`
                ).join("");
            }
        }

        // Update Blockchain Explorer Ledger
        const blockContainer = document.getElementById("blocks");
        if (blockContainer && data.blocks) {
            document.querySelectorAll("[data-blocks]").forEach(el => el.textContent = data.blocks.length);
            blockContainer.innerHTML = data.blocks.map(b =>
                `<div class="block">
                    <div class="block-head">
                        <strong>Block #${b.index}</strong>
                        <span class="badge">Valid</span>
                    </div>
                    <div class="small">Previous Hash: ${b.prev.substring(0, 24)}...</div>
                    <div class="hash">Hash: ${b.hash}</div>
                    <div class="stat"><span>Data</span><strong>${b.data}</strong></div>
                    <div class="small">Timestamp: ${b.time}</div>
                </div>`
            ).join("");
        }
    } catch (err) {
        // Ecosystem sync catch
    }
}
'''

with open("script.js", "w") as f:
    f.write(script_js)

print("script.js updated with Tomcat Servlet endpoints!")
