script_js = '''const API_URL = "/BitForge/api";
const currentUser = localStorage.getItem("bitforgeUser") || "bhanu@gmail.com";

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-user]").forEach(el => {
        el.textContent = currentUser;
    });

    const targetUser = localStorage.getItem("selectedPayTarget");
    if (targetUser) {
        const recField = document.getElementById("receiver");
        if (recField) recField.value = targetUser;
        localStorage.removeItem("selectedPayTarget");
    }
    
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

// 1. Ecosystem Data Sync
async function fetchEcosystemData() {
    try {
        // Fetch Exact Database User Balance & Privacy Status from MySQL
        const resUser = await fetch(`${API_URL}/user?email=${encodeURIComponent(currentUser)}`);
        const userData = await resUser.json();
        
        const balEl = document.getElementById("userBalance");
        const visBtn = document.getElementById("visibilityBtn");

        if (userData.success && balEl) {
            if (userData.is_private) {
                balEl.textContent = "••••••";
                if (visBtn) {
                    visBtn.textContent = "🔒 Visibility: Private (Hidden)";
                    visBtn.classList.add("private");
                }
            } else {
                balEl.textContent = userData.balance.toFixed(2);
                if (visBtn) {
                    visBtn.textContent = "👁️ Visibility: Public";
                    visBtn.classList.remove("private");
                }
            }
        }

        const res = await fetch(`${API_URL}/transactions`);
        const data = await res.json();

        // Render People Grid
        const peopleGrid = document.getElementById("peopleGrid");
        if (peopleGrid && data.users) {
            const contacts = data.users.filter(u => u.email.toLowerCase() !== currentUser.toLowerCase());
            if (contacts.length === 0) {
                peopleGrid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; opacity: 0.7;">No other contacts registered yet.</div>';
            } else {
                peopleGrid.innerHTML = contacts.map(u => {
                    const initial = u.email.charAt(0).toUpperCase();
                    const shortName = u.email.split("@")[0];
                    return `
                        <div class="contact-avatar" onclick="selectContact('${u.email}')">
                            <div class="avatar-circle">${initial}</div>
                            <div class="contact-name">${shortName}</div>
                        </div>
                    `;
                }).join("");
            }
        }

        // Render Transactions Table
        const txBody = document.getElementById("txBody");
        if (txBody && data.transactions) {
            if (data.transactions.length === 0) {
                txBody.innerHTML = '<tr><td colspan="4" style="padding: 15px; text-align: center;">No transactions recorded.</td></tr>';
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
    } catch (err) {}
}

async function toggleBalanceVisibility() {
    const visBtn = document.getElementById("visibilityBtn");
    const isCurrentlyPrivate = visBtn && visBtn.classList.contains("private");
    const newToggle = !isCurrentlyPrivate;

    try {
        await fetch(`${API_URL}/user`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `email=${encodeURIComponent(currentUser)}&toggle=${newToggle}`
        });
        fetchEcosystemData();
    } catch (err) {}
}

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
'''

with open("script.js", "w") as f:
    f.write(script_js)
print("script.js updated!")
