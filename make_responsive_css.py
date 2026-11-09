css = '''* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #0f172a;
    color: #f8fafc;
    min-height: 100vh;
}

nav {
    background: #1e293b;
    padding: 15px 20px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    border-bottom: 2px solid #00d2ff;
}

nav a {
    color: #94a3b8;
    text-decoration: none;
    font-weight: 600;
    padding: 8px 12px;
    border-radius: 6px;
    transition: all 0.2s;
}

nav a:hover, nav a.active {
    color: #00d2ff;
    background: rgba(0, 210, 255, 0.1);
}

.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 20px 15px;
}

/* Dynamic Grid Layouts */
.grid-2, .grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

/* Card Styling */
.stat-card, .wallet-card, .pay-card, .net-card {
    border: 1px solid #00d2ff;
    padding: 20px;
    border-radius: 12px;
    background: rgba(0, 210, 255, 0.05);
    word-break: break-word;
}

/* Responsive Table Wrapper */
.table-responsive {
    width: 100%;
    overflow-x: auto;
    margin-top: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 500px;
}

th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

th {
    border-bottom: 2px solid #00d2ff;
    color: #00d2ff;
}

/* Mobile Screen Adjustments (Phones < 600px) */
@media (max-width: 600px) {
    nav {
        flex-direction: column;
        align-items: stretch;
        text-align: center;
    }
    nav a {
        display: block;
        padding: 10px;
    }
    .pay-card, .wallet-card {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }
    .action-group {
        flex-direction: column;
        width: 100%;
    }
    .btn-inspect, .btn-pay {
        width: 100%;
        margin-top: 5px;
    }
}
'''

with open("style.css", "w") as f:
    f.write(css)
print("style.css updated for mobile responsiveness!")
