with open("script.js", "r") as f:
    code = f.read()

# Add Toast Notification Core Functions
toast_system_code = '''
// Global Toast Alert Container & Trigger
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
'''

# Inject toast monitoring inside fetchEcosystemData
monitoring_code = '''
        // Real-time Incoming BFG Notification Tracker
        if (data.transactions) {
            if (lastKnownTxCount !== -1 && data.transactions.length > lastKnownTxCount) {
                const latestTx = data.transactions[0]; // newest transaction
                if (latestTx.to.toLowerCase() === currentUser.toLowerCase() && latestTx.from.toLowerCase() !== currentUser.toLowerCase()) {
                    showToast(`You just received +${latestTx.amount} BFG from ${latestTx.from}!`, "received");
                }
            }
            lastKnownTxCount = data.transactions.length;
        }
'''

if "function showToast(" not in code:
    code = toast_system_code + "\n" + code

if "lastKnownTxCount !== -1" not in code:
    code = code.replace("const txBody = document.getElementById(\"txBody\");", monitoring_code + "\n        const txBody = document.getElementById(\"txBody\");")

if "showMessage(data.message, !data.success);" in code:
    code = code.replace(
        "showMessage(data.message, !data.success);",
        'showMessage(data.message, !data.success);\n        if (data.success) showToast(`Successfully sent BFG to ${receiver}!`, "success");'
    )

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with real-time notification engine!")
