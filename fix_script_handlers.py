script_js = '''const API_URL = window.location.origin + "/BitForge/api";
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
    
    if (document.getElementById("userBalance") || document.getElementById("peopleGrid")) {
        fetchEcosystemData();
        setInterval(fetchEcosystemData, 2000);
    }
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

// Global Authentication Functions
window.handleLogin = async function(event) {
    if (event) event.preventDefault();
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
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value;
    const confirm = document.getElementById("signupConfirm").value;
    const question = document.getElementById("secretQuestion").value;
    const answer = document.getElementById("secretAnswer").value;

    if (password !== confirm) {
        showMessage("Passwords do not match!", true);
        return false;
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
    return false;
};

// Ecosystem Sync
async function fetchEcosystemData() {
    try {
        const resUser = await fetch(`${API_URL}/user?email=${encodeURIComponent(currentUser)}`);
        const userData = await resUser.json();
        
        const balEl = document.getElementById("userBalance");
        const visBtn = document.getElementById("visibilityBtn");

        if (userData.success && balEl) {
            if (userData.is_private) {
                balEl.textContent = "••••••";
                if (visBtn) {
                    visBtn.textContent = "🔒 Visibility: Private (Hidden)";
                    visBtn.style.background = "#e74c3c";
                }
            } else {
                balEl.textContent = userData.balance.toFixed(2);
                if (visBtn) {
                    visBtn.textContent = "👁️ Visibility: Public";
                    visBtn.style.background = "#34495e";
                }
            }
        }

        const res = await fetch(`${API_URL}/transactions`);
        const data = await res.json();

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
            body: `email=${encodeURIComponent(currentUser)}&toggle=${newToggle}`
        });
        fetchEcosystemData();
    } catch (err) {}
};

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
    if (event) event.preventDefault();
    const receiver = document.getElementById("receiver").value.trim();
    const amount = Number(document.getElementById("amount").value);
    executePayment(receiver, amount);
}
'''

with open("script.js", "w") as f:
    f.write(script_js)

print("script.js updated!")
