with open("html/transactions.html", "r") as f:
    html_code = f.read()

target_old_func = """function submitQRPopupPayment(event) {
            event.preventDefault();
            const amount = Number(document.getElementById("popupAmount").value);
            
            if (!scannedTargetEmail || amount <= 0) {
                alert("Please enter a valid amount.");
                return;
            }

            // Close popup and execute backend transfer
            closeQRPayModal();
            executePayment(scannedTargetEmail, amount);
        }"""

target_new_func = """function submitQRPopupPayment(event) {
            if (event) event.preventDefault();
            const amountInput = document.getElementById("popupAmount");
            const amount = Number(amountInput ? amountInput.value : 0);
            
            if (!scannedTargetEmail || amount <= 0) {
                showMessage("Please enter a valid positive amount.", true);
                return false;
            }

            closeQRPayModal();
            window.executePayment(scannedTargetEmail, amount);
            return false;
        }"""

if target_old_func in html_code:
    html_code = html_code.replace(target_old_func, target_new_func)

with open("html/transactions.html", "w") as f:
    f.write(html_code)

print("html/transactions.html updated with direct window execution!")
