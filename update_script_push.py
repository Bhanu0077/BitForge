with open("script.js", "r") as f:
    code = f.read()

push_init = '''
// Register PWA Service Worker & Push Notification Permission
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('../sw.js').catch(err => {});
}

function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission !== 'granted') {
        Notification.requestPermission();
    }
}
'''

# Trigger OS System Notification
native_notify_func = '''
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
'''

if "requestNotificationPermission" not in code:
    code = push_init + "\n" + native_notify_func + "\n" + code

# Update real-time transaction handler to fire system notifications
if "showToast(`You just received +" in code:
    code = code.replace(
        'showToast(`You just received +${latestTx.amount} BFG from ${latestTx.from}!`, "received");',
        'showToast(`You just received +${latestTx.amount} BFG from ${latestTx.from}!`, "received");\n                    triggerSystemNotification("💰 BFG Received!", `You just received +${latestTx.amount} BFG from ${latestTx.from}!`);'
    )

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with Native Notification Support!")
