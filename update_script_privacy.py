with open("script.js", "r") as f:
    code = f.read()

# Update balance calculation display logic
old_bal_code = 'if (balEl) balEl.textContent = balance.toFixed(2);'
new_bal_code = '''if (balEl) {
                const isPrivate = localStorage.getItem("balancePrivate") === "true";
                balEl.textContent = isPrivate ? "••••••" : balance.toFixed(2);
            }'''

if old_bal_code in code:
    code = code.replace(old_bal_code, new_bal_code)

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with balance privacy check!")
