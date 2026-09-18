const currentUser = localStorage.getItem("bitforgeUser") || "Bhanu";

document.querySelectorAll("[data-user]").forEach(el => {
  el.textContent = currentUser;
});

function saveUser() {
  const name = document.getElementById("name")?.value.trim();
  if (!name) return;
  localStorage.setItem("bitforgeUser", name);
  location.href = "index.html";
}

function logout() {
  localStorage.removeItem("bitforgeUser");
  location.href = "login.html";
}

function showMessage(text) {
  const box = document.getElementById("message");
  if (box) box.textContent = text;
}

function sendCoins(event) {
  event.preventDefault();
  const receiver = document.getElementById("receiver").value.trim();
  const amount = Number(document.getElementById("amount").value);

  if (!receiver || amount <= 0) {
    showMessage("Please enter a valid receiver and amount.");
    return;
  }

  const transactions = JSON.parse(localStorage.getItem("bitforgeTxs") || "[]");
  transactions.unshift({
    from: currentUser,
    to: receiver,
    amount: amount,
    time: new Date().toLocaleString()
  });
  localStorage.setItem("bitforgeTxs", JSON.stringify(transactions));

  showMessage("Transaction created. Go to Mining to add it to a block.");
  event.target.reset();
}

function renderTransactions() {
  const body = document.getElementById("txBody");
  if (!body) return;

  const txs = JSON.parse(localStorage.getItem("bitforgeTxs") || "[]");
  if (!txs.length) {
    body.innerHTML = '<tr><td colspan="4">No transactions yet.</td></tr>';
    return;
  }

  body.innerHTML = txs.map(t =>
    `<tr><td>${t.from}</td><td>${t.to}</td><td>${t.amount} BFG</td><td>${t.time}</td></tr>`
  ).join("");
}

function addBlock() {
  const blocks = Number(localStorage.getItem("bitforgeBlocks") || 1) + 1;
  localStorage.setItem("bitforgeBlocks", blocks);
  document.querySelectorAll("[data-blocks]").forEach(el => el.textContent = blocks);
  showMessage("Block #" + blocks + " mined successfully — network only.");
}

function renderBlocks() {
  const container = document.getElementById("blocks");
  if (!container) return;

  const count = Number(localStorage.getItem("bitforgeBlocks") || 1);
  let html = "";

  for (let i = count; i >= 1; i--) {
    html += `
      <div class="block">
        <div class="block-head">
          <strong>Block #${i}</strong>
          <span class="badge">Valid</span>
        </div>
        <div class="small">Previous Hash</div>
        <div class="hash">000000000000000000000000000000000000000000000000000000000000${i}</div>
        <div class="stat"><span>Transactions</span><strong>${i === 1 ? 0 : 1}</strong></div>
      </div>`;
  }
  container.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
  renderTransactions();
  renderBlocks();
  document.querySelectorAll("[data-blocks]").forEach(el => {
    el.textContent = localStorage.getItem("bitforgeBlocks") || "1";
  });
});
