// Simple BitForge UI JavaScript.
// This project uses localStorage only for a small demo login.

const menuButton = document.getElementById("menu-button");
const navigation = document.getElementById("main-nav");
const messageBox = document.getElementById("message");

if (menuButton && navigation) {
    menuButton.addEventListener("click", function () {
        navigation.classList.toggle("open");
    });
}

function showMessage(text) {
    if (!messageBox) {
        alert(text);
        return;
    }
    messageBox.textContent = text;
    messageBox.classList.add("show");
    setTimeout(function () {
        messageBox.classList.remove("show");
    }, 2500);
}

const savedName = localStorage.getItem("bitforgeUser");
document.querySelectorAll("#welcome-user").forEach(function (item) {
    item.textContent = savedName ? "Hi, " + savedName : "Guest";
});

const loginForm = document.getElementById("login-form");
if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const email = document.getElementById("login-email").value;
        const name = email.split("@")[0];
        localStorage.setItem("bitforgeUser", name);
        window.location.href = "index.html";
    });
}

const signupForm = document.getElementById("signup-form");
if (signupForm) {
    signupForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const name = document.getElementById("signup-name").value;
        localStorage.setItem("bitforgeUser", name);
        showMessage("Account created successfully!");
        setTimeout(function () {
            window.location.href = "index.html";
        }, 800);
    });
}

const sendForm = document.getElementById("send-form");
if (sendForm) {
    sendForm.addEventListener("submit", function (event) {
        event.preventDefault();
        showMessage("Transfer submitted! This is only a demo.");
        sendForm.reset();
    });
}

const mineButton = document.getElementById("mine-button");
if (mineButton) {
    mineButton.addEventListener("click", function () {
        showMessage("Mining started... Demo only.");
    });
}

const verifyButton = document.getElementById("verify-button");
if (verifyButton) {
    verifyButton.addEventListener("click", function () {
        showMessage("Blockchain verified! Demo result.");
    });
}

function logoutUser() {
    localStorage.removeItem("bitforgeUser");
}
