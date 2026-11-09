with open("script.js", "r") as f:
    code = f.read()

# Replace hardcoded API URL with dynamic origin resolution
old_url = 'const API_URL = "/BitForge/api";'
new_url = 'const API_URL = window.location.origin + "/BitForge/api";'

if old_url in code:
    code = code.replace(old_url, new_url)

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with dynamic origin resolution!")
