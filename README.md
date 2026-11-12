# BitForge

A simple blockchain dashboard made with HTML, CSS and JavaScript.

## Pages
- Login / Signup
- Dashboard
- Wallet
- Transactions
- Mining
- Blockchain
- Network
- Administrator console (`html/admin-login.html`)

## Technologies
HTML, CSS, JavaScript and localStorage.

Open `html/login.html` to start.

## Administrator console

The administrator console is a separate, session-protected interface for viewing
the live `users`, `transactions`, and `blockchain` tables. It can create and
edit users, remove users and their related transaction rows, and edit or remove
transaction records. Blockchain rows are deliberately read-only so an admin
cannot silently break the chain's hash history. Transaction edits are audit
record edits and do not recalculate wallet balances.

Configure administrator credentials on the Tomcat process before opening
`html/admin-login.html`. BitForge deliberately has no default administrator
credentials.

```bash
export BITFORGE_ADMIN_USERNAME=admin
export BITFORGE_ADMIN_PASSWORD='use-a-long-unique-password'
```

Restart Tomcat after changing the credentials.
