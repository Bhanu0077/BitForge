script_js = '''const API_URL = window.location.origin + "/BitForge/api";
const currentUser = localStorage.getItem("bitforgeUser") || "demo_user";

let lastKnownTxCount = -1;

function showToast(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    let icon = "🔔";
    if (type === "success") icon = "✅";
    if (type === "received") icon = "💰";
    if (type === "error") icon = "⚠️";

    toast.innerHTML = `
        <div><strong>${icon} Notification:</strong> ${message}</div>
        <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = "fadeOut 0.3s ease-in forwards";
        setTimeout(() => toast.remove(), 300);
    }, 4500);
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('../sw.js').catch(err => {});
}

function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission !== 'granted') {
        Notification.requestPermission();
    }
}

function triggerSystemNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        try {
            new Notification(title, {
                body: message,
                icon: "https://cdn-icons-png.flaticon.com/512/2091/2091665.png"
            });
        } catch(e) {}
    }
}

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

window.togglePasswordVisibility = function(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === "password") {
        input.type = "text";
        btn.textContent = "🙈";
    } else {
        input.type = "password";
        btn.textContent = "👁️";
    }
};

window.handleLogin = async function(event) {
    if (event) event.preventDefault();
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value;

    const payload = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();

        if (data.success) {
            localStorage.setItem("bitforgeUser", data.username);
            showMessage("Login successful! Redirecting...");
            setTimeout(() => { window.location.href = "index.html"; }, 800);
        } else {
            showMessage(data.message || "Invalid credentials", true);
        }
    } catch (err) {
        showMessage("Connection to Tomcat server failed.", true);
    }
    return false;
};

window.handleSignup = async function(event) {
    if (event) event.preventDefault();
    const username = document.getElementById("signupUsername").value.trim();
    const password = document.getElementById("signupPassword").value;
    const confirm = document.getElementById("signupConfirm").value;
    const question = document.getElementById("secretQuestion").value;
    const answer = document.getElementById("secretAnswer").value;

    if (password !== confirm) {
        showMessage("Passwords do not match!", true);
        return false;
    }

    const payload = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&question=${encodeURIComponent(question)}&answer=${encodeURIComponent(answer)}`;
    
    try {
        const res = await fetch(`${API_URL}/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload
        });
        const data = await res.json();
        
        if (data.success) {
            showMessage("Account created! Wallet initialized with 100 BFG. Redirecting to login...");
            setTimeout(() => window.location.href = "login.html", 1200);
        } else {
            showMessage(data.message, true);
        }
    } catch (err) {
        showMessage("Tomcat backend connection error.", true);
    }
    return false;
};

window.handleForgotPassword = async function(event) {
    if (event) event.preventDefault();
    const username = document.getElementById("forgotUsername").value.trim();
    const answer = document.getElementById("forgotAnswer").value;
    const newPassword = document.getElementById("forgotNewPassword").value;

    const payload = `username=${encodeURIComponent(username)}&answer=${encodeURIComponent(answer)}&new_password=${encodeURIComponent(newPassword)}`;

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
    return false;
};

async function fetchEcosystemData() {
    try {
        const resUser = await fetch(`${API_URL}/user?username=${encodeURIComponent(currentUser)}`);
        const userData = await resUser.json();
        
        const balEl = document.getElementById("userBalance");
        const visBtn = document.getElementById("visibilityBtn");

        if (userData.success && balEl) {
            balEl.textContent = userData.balance.toFixed(2);
            if (visBtn) {
                if (userData.is_private) {
                    visBtn.textContent = "🔒 Visibility: Private";
                    visBtn.style.background = "#e74c3c";
                } else {
                    visBtn.textContent = "👁️ Visibility: Public";
                    visBtn.style.background = "#34495e";
                }
            }
        }

        const res = await fetch(`${API_URL}/transactions`);
        const data = await res.json();

        if (data.transactions) {
            if (lastKnownTxCount !== -1 && data.transactions.length > lastKnownTxCount) {
                const latestTx = data.transactions[0];
                if (latestTx.to.toLowerCase() === currentUser.toLowerCase() && latestTx.from.toLowerCase() !== currentUser.toLowerCase()) {
                    showToast(`You just received +${latestTx.amount} BFG from ${latestTx.from}!`, "received");
                    triggerSystemNotification("💰 BFG Received!", `You just received +${latestTx.amount} BFG from ${latestTx.from}!`);
                }
            }
            lastKnownTxCount = data.transactions.length;
        }

        const peopleGrid = document.getElementById("peopleGrid");
        if (peopleGrid && data.users) {
            const contacts = data.users.filter(u => u.username.toLowerCase() !== currentUser.toLowerCase());
            if (contacts.length === 0) {
                peopleGrid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; opacity: 0.7;">No other registered users in directory.</div>';
            } else {
                peopleGrid.innerHTML = contacts.map(u => {
                    const initial = u.username.charAt(0).toUpperCase();
                    return `
                        <div class="contact-avatar" onclick="selectContact('${u.username}')">
                            <div class="avatar-circle">${initial}</div>
                            <div class="contact-name">${u.username}</div>
                        </div>
                    `;
                }).join("");
            }
        }

        const txBody = document.getElementById("txBody");
        if (txBody && data.transactions) {
            if (data.transactions.length === 0) {
                txBody.innerHTML = '<tr><td colspan="4" style="padding: 15px; text-align: center;">No transactions recorded yet.</td></tr>';
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

        const blockContainer = document.getElementById("blocks");
        if (blockContainer && data.blocks) {
            document.querySelectorAll("[data-blocks]").forEach(el => el.textContent = data.blocks.length);
            blockContainer.innerHTML = data.blocks.map(b =>
                `<div class="block" style="border: 1px solid #00d2ff; padding: 18px; margin-bottom: 15px; border-radius: 10px; background: rgba(0, 210, 255, 0.03);">
                    <div class="block-head" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,210,255,0.2); padding-bottom: 8px;">
                        <strong style="color: #00d2ff; font-size: 1.1rem;">Block #${b.index}</strong>
                        <span class="badge" style="background: #27ae60; color: #fff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;">● Validated</span>
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 10px;"><strong>Previous Hash:</strong> <span style="font-family: monospace;">${b.prev}</span></div>
                    <div style="font-family: monospace; color: #00d2ff; margin: 6px 0; word-break: break-all;"><strong>Current Hash:</strong> ${b.hash}</div>
                    <div style="margin-top: 6px;"><span>Transactions / Payload: </span><strong style="color: #2ecc71;">${b.data}</strong></div>
                    <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 8px;">Mined Timestamp: ${b.time}</div>
                </div>`
            ).join("");
        }
    } catch (err) {}
}

window.toggleBalanceVisibility = async function() {
    const visBtn = document.getElementById("visibilityBtn");
    const isPrivateNow = visBtn && visBtn.textContent.includes("Private");
    const newToggle = !isPrivateNow;

    try {
        await fetch(`${API_URL}/user`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `username=${encodeURIComponent(currentUser)}&toggle=${newToggle}`
        });
        fetchEcosystemData();
    } catch (err) {}
};

window.executePayment = async function(receiver, amount) {
    if (!receiver || amount <= 0) {
        showMessage("Please enter a valid receiver username and positive amount.", true);
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
        if (data.success) {
            showToast(`Successfully sent ${amount} BFG to ${receiver}!`, "success");
        }
        fetchEcosystemData();
    } catch (err) {
        showMessage("Transaction failed to process.", true);
    }
};

window.sendCoins = function(event) {
    if (event) event.preventDefault();
    const receiver = document.getElementById("receiver").value.trim();
    const amount = Number(document.getElementById("amount").value);
    window.executePayment(receiver, amount);
};
'''

with open("script.js", "w") as f:
    f.write(script_js)

print("script.js updated for usernames!")
