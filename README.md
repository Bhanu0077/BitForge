# BitForge

<p align="center">
  <strong>A local-first Bitcoin-inspired wallet, mining engine, and blockchain ledger.</strong>
</p>

BitForge is a Tomcat-hosted web application that demonstrates the flow of a digital coin ecosystem: create a wallet account, mine proof-of-work blocks, transfer coins, inspect the ledger, and monitor network activity. The interface runs on HTML, CSS, and JavaScript, while MySQL and Java Jakarta Servlets provide persistent accounts and blockchain records.

> BitForge is an educational simulation. It is not a cryptocurrency, does not connect to the Bitcoin network, and is not intended for real financial use.

## Features

- Zero starting balance for every newly created account
- 50 BFG reward for the first mining reward era
- Reward halving every 210 newly mined blocks: 50 → 25 → 12.5 → ...
- Hardware-aware mining duration using browser CPU, memory, GPU, randomness, and the selected mining work loop
- Transactions assigned immediately to the newest mined block
- Empty mined blocks remain valid ledger entries
- Inspectable blocks containing transaction sender, receiver, amount, and timestamp
- Dashboard, wallet, payments, mining, ledger, network, and administrator views
- Persistent MySQL-backed users, balances, transactions, and block data
- No continuous ledger or dashboard polling

## Project pages

| Page | Purpose |
|---|---|
| `html/login.html` | Sign in |
| `html/signup.html` | Create a wallet with a 0 BFG balance |
| `html/index.html` | Dashboard, balance, chain status, and recent activity |
| `html/wallet.html` | Wallet details and QR code |
| `html/transactions.html` | Send or receive coins and view payment activity |
| `html/mining.html` | Mine a block with the client hardware |
| `html/blockchain.html` | Inspect each block and its transactions |
| `html/network.html` | Network and peer information |
| `html/admin-login.html` | Secure administrator console |

## Technology stack

- Java 21
- Jakarta Servlet API / Apache Tomcat 11
- MySQL 8 or MariaDB compatible with MySQL JDBC
- MySQL Connector/J
- HTML5, CSS3, and vanilla JavaScript
- Browser Storage and Service Worker support

## Repository layout

```text
BitForge/
├── html/                 # Web pages
├── src/com/bitforge/     # Java servlet source files
├── WEB-INF/
│   ├── lib/              # JDBC and application libraries
│   ├── classes/          # Compiled classes generated from src/
│   └── web.xml           # Jakarta web application configuration
├── script.js             # Shared dashboard and payment logic
├── style.css             # Shared interface styles
└── README.md
```

## Prerequisites

Install or provide:

- Apache Tomcat 11.0.27 or compatible Jakarta EE 10+ Tomcat
- Java 21 JDK
- MySQL server
- A modern browser with JavaScript enabled
- Optional: Git and GitHub CLI or HTTPS credentials

## First-time setup

### 1. Clone the project

```bash
cd ~
git clone https://github.com/Bhanu0077/BitForge.git
cd BitForge
```

### 2. Create the MySQL database and application user

By default, `DatabaseManager.java` uses:

```text
Host:     localhost
Port:     3306
Database: bitforge_db
Username: bitforge
Password: bitforge123
```

Connect to MySQL as an administrator and run:

```sql
CREATE DATABASE IF NOT EXISTS bitforge_db;
CREATE USER IF NOT EXISTS 'bitforge'@'localhost'
  IDENTIFIED BY 'bitforge123';
GRANT ALL PRIVILEGES ON bitforge_db.* TO 'bitforge'@'localhost';
FLUSH PRIVILEGES;
```

To use different credentials, update the constants in:

```text
src/com/bitforge/DatabaseManager.java
```

### 3. Install the application in Tomcat

The deployed web application directory is:

```text
~/apache-tomcat-11.0.27/webapps/BitForge
```

From the project directory, compile all servlet sources using Tomcat's Servlet API and the application's JDBC libraries:

```bash
javac -cp "/home/$USER/apache-tomcat-11.0.27/lib/*:/home/$USER/apache-tomcat-11.0.27/webapps/BitForge/WEB-INF/lib/*" \
  -d /home/$USER/apache-tomcat-11.0.27/webapps/BitForge/WEB-INF/classes \
  src/com/bitforge/*.java
```

Copy the web files into the deployed application:

```bash
cp -a html/. /home/$USER/apache-tomcat-11.0.27/webapps/BitForge/html/
cp -a script.js style.css manifest.json sw.js \
  /home/$USER/apache-tomcat-11.0.27/webapps/BitForge/
```

If the deployed application does not exist yet, copy the complete project directory before compiling:

```bash
cp -a ~/BitForge /home/$USER/apache-tomcat-11.0.27/webapps/
```

### 4. Configure administrator credentials

BitForge has no built-in administrator password. Set credentials on the Tomcat process before starting it.

Linux shell:

```bash
export BITFORGE_ADMIN_USERNAME='your-admin-name'
export BITFORGE_ADMIN_PASSWORD='use-a-long-unique-password'
```

Persistent Tomcat configuration:

```bash
cat > ~/apache-tomcat-11.0.27/bin/setenv.sh <<'EOF'
export BITFORGE_ADMIN_USERNAME='your-admin-name'
export BITFORGE_ADMIN_PASSWORD='use-a-long-unique-password'
EOF
chmod +x ~/apache-tomcat-11.0.27/bin/setenv.sh
```

Never commit real administrator credentials to Git.

### 5. Start MySQL and Tomcat

```bash
sudo systemctl start mysql
/home/$USER/apache-tomcat-11.0.27/bin/catalina.sh start
```

Open:

```text
http://localhost:8080/BitForge/
```

Tomcat initializes the schema automatically on startup. It creates or migrates the users, transactions, and blockchain tables and supplies the application with a clean genesis block when appropriate.

## Starting after every code change

Compile the Java sources:

```bash
cd ~/BitForge
javac -cp "/home/$USER/apache-tomcat-11.0.27/lib/*:/home/$USER/apache-tomcat-11.0.27/webapps/BitForge/WEB-INF/lib/*" \
  -d /home/$USER/apache-tomcat-11.0.27/webapps/BitForge/WEB-INF/classes \
  src/com/bitforge/*.java
```

Deploy web resources:

```bash
cp -a html/. /home/$USER/apache-tomcat-11.0.27/webapps/BitForge/html/
cp script.js style.css manifest.json sw.js /home/$USER/apache-tomcat-11.0.27/webapps/BitForge/
```

Restart Tomcat:

```bash
/home/$USER/apache-tomcat-11.0.27/bin/catalina.sh stop
/home/$USER/apache-tomcat-11.0.27/bin/catalina.sh start
```

## Blockchain behavior

### Genesis block

The first block is block 1, a genesis block with no normal transaction activity.

### Mining rewards

Each newly mined block receives a reward according to the block index:

| Blocks | Reward |
|---|---:|
| 2–211 | 50 BFG |
| 212–421 | 25 BFG |
| 422–631 | 12.5 BFG |
| ... | Halves every 210 blocks |

The reward is credited only after the block and miner balance update commit successfully.

### Mining speed

Mining duration is determined in the browser from:

- Logical CPU cores reported by `navigator.hardwareConcurrency`
- Approximate device memory reported by `navigator.deviceMemory`
- Whether WebGL/GPU access is available
- Random timing variation

A more capable client can generally finish the local proof-of-work timing loop faster, and two miners do not need to finish at the same instant.

### Transaction placement

Each successful payment is written into MySQL with the current newest block index. The transaction therefore appears in that block until a miner creates the next block. Transactions are not held in a separate frontend queue and are not assigned only by browser refresh.

## Resetting the project

To erase every user, balance, transaction, and mined block and start from the beginning:

```bash
sudo systemctl start mysql

mysql -h 127.0.0.1 -u bitforge -pbitforge123 bitforge_db <<'SQL'
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE transactions;
TRUNCATE TABLE blockchain;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO blockchain
(block_index, previous_hash, current_hash, nonce, transactions_data)
VALUES (
  1,
  '00000000000000000000000000000000',
  '0000a1b2c3d4e5f67890123456789012',
  0,
  'Genesis Block'
);
SQL
```

Then clear browser site data for:

```text
http://localhost:8080
```

This removes the cached local user identity and causes the next visit to start at login/signup.

## Running checks

Check the deployed application:

```bash
curl -I http://localhost:8080/BitForge/
curl http://localhost:8080/BitForge/api/blockchain
curl http://localhost:8080/BitForge/api/transactions
curl http://localhost:8080/BitForge/api/network
```

Useful Tomcat logs:

```bash
tail -n 100 ~/apache-tomcat-11.0.27/logs/catalina.out
```

Useful processes:

```bash
ps -ef | grep '[o]rg.apache.catalina.startup.Bootstrap'
mysqladmin ping -h localhost -u bitforge -pbitforge123
```

## Stopping the project

```bash
/home/$USER/apache-tomcat-11.0.27/bin/catalina.sh stop
sudo systemctl stop mysql
```

## GitHub workflow

Create a feature or improvement commit:

```bash
cd ~/BitForge
git status
git add .
git diff --cached --check
git commit -m "Describe your BitForge change"
git push origin main
```

Do not commit database credentials or compiled `.class` files. The repository ignores `*.class` and `WEB-INF/classes/`.

## Administrator console

Open:

```text
http://localhost:8080/BitForge/html/admin-login.html
```

The console can:

- Create and edit users
- Change wallet balances
- Remove users and associated transactions
- Inspect and remove transaction records
- Inspect blockchain records

Blockchain rows remain read-only through the administrator interface to prevent accidental modification of chain history.

## Troubleshooting

### Tomcat cannot connect to MySQL

Check that MySQL is running:

```bash
sudo systemctl status mysql
```

Test the configured account:

```bash
mysql -h 127.0.0.1 -u bitforge -pbitforge123 bitforge_db
```

### Page is old or not updated

Perform a hard refresh, or clear the BitForge site data in browser developer tools. JavaScript changes must also be copied into Tomcat's deployed `BitForge` directory.

### Java compilation reports a missing Servlet API

Compile against Tomcat's `lib` directory:

```bash
cp=/home/$USER/apache-tomcat-11.0.27/lib/*
```

Include that directory in the `javac -cp` command.

### Port 8080 is already used

Stop the existing Tomcat instance:

```bash
/home/$USER/apache-tomcat-11.0.27/bin/catalina.sh stop
```

Then start it again.

## License

Educational and experimental use. Add a license file if the project is intended for public distribution under specific terms.
