// BitForge UI foundation JavaScript.
// Future versions can replace these messages with real PHP/API requests.

const menuButton = document.getElementById("menu-button");
const navigation = document.getElementById("main-nav");
const messageBox = document.getElementById("message");
const sendForm = document.getElementById("send-form");

// Opens the simple mobile navigation menu.
menuButton.addEventListener("click", function () {
    const isOpen = navigation.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", isOpen);
});

// Shows a small notice for UI-only buttons.
function showMessage(text) {
    messageBox.textContent = text;
    messageBox.classList.add("show");

    setTimeout(function () {
        messageBox.classList.remove("show");
    }, 3500);
}

document.querySelectorAll("[data-message]").forEach(function (button) {
    button.addEventListener("click", function () {
        showMessage(button.dataset.message);
    });
});

// This validates only that fields have been filled in. It sends nothing.
sendForm.addEventListener("submit", function (event) {
    event.preventDefault();

    if (sendForm.checkValidity()) {
        showMessage("This is a UI demo. Real transactions will be added later.");
        sendForm.reset();
    } else {
        showMessage("Please enter a recipient wallet and an amount.");
    }
});
