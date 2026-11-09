# 1. Create Web App Manifest
manifest = '''{
  "name": "BitForge Wallet",
  "short_name": "BitForge",
  "start_url": "../html/index.html",
  "display": "standalone",
  "background_color": "#0f172a",
  "theme_color": "#00d2ff",
  "icons": [
    {
      "src": "https://cdn-icons-png.flaticon.com/512/2091/2091665.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}'''

with open("manifest.json", "w") as f:
    f.write(manifest)

# 2. Create Service Worker Script for Push Handling
sw_js = '''self.addEventListener("push", (event) => {
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
'''

with open("sw.js", "w") as f:
    f.write(sw_js)

print("manifest.json and sw.js created!")
