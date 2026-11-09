self.addEventListener("push", (event) => {
    const data = event.data ? event.data.json() : {};
    const title = data.title || "BitForge Wallet";
    const options = {
        body: data.body || "New transaction update received!",
        icon: "https://cdn-icons-png.flaticon.com/512/2091/2091665.png",
        badge: "https://cdn-icons-png.flaticon.com/512/2091/2091665.png",
        vibrate: [200, 100, 200]
    };
    event.waitUntil(self.registration.showNotification(title, options));
});
