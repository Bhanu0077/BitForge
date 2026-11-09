with open("script.js", "r") as f:
    code = f.read()

# Auto-fill selected target if coming from Network tab
auto_select_patch = '''
    const targetUser = localStorage.getItem("selectedPayTarget");
    if (targetUser) {
        const recField = document.getElementById("receiver");
        if (recField) recField.value = targetUser;
        localStorage.removeItem("selectedPayTarget");
    }
'''

if "selectedPayTarget" not in code:
    code = code.replace('document.addEventListener("DOMContentLoaded", () => {', 'document.addEventListener("DOMContentLoaded", () => {' + auto_select_patch)

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with auto-target selection handler!")
