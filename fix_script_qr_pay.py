with open("script.js", "r") as f:
    code = f.read()

# Make sure executePayment is globally exposed
if "window.executePayment =" not in code:
    code = code.replace("async function executePayment(", "window.executePayment = async function executePayment(")

if "window.sendCoins =" not in code:
    code = code.replace("function sendCoins(", "window.sendCoins = function sendCoins(")

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with global payment execution bindings!")
