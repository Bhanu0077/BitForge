# BitForge

BitForge is a lightweight educational blockchain dashboard built with HTML, CSS, and JavaScript. It presents a simplified crypto-style interface for exploring a wallet, transaction activity, mining preview, blockchain layout, and network status without using real cryptocurrency.

## Overview

This project is designed as a frontend demo for learning how blockchain-inspired UI concepts can be structured in a web app. It includes:

- a wallet summary with balance and wallet address
- a transfer form UI
- mining and transaction statistics
- a recent transactions table
- a blockchain preview section
- a simple network status display
- responsive layout for desktop and mobile screens

## Project Structure

- `index.html` — main dashboard markup
- `style.css` — styling and responsive layout
- `script.js` — basic UI interactions and demo messaging

## Features

- Modern dashboard styling with a blockchain-inspired theme
- Responsive navigation and mobile menu
- Interactive demo buttons with status messages
- Form validation for the send-coin mock experience
- Placeholder data to help visualize blockchain-related features

## Run Locally

You can open the project in a browser directly:

1. Open `index.html` in your browser, or
2. Serve the folder locally with a simple HTTP server:

```bash
cd BitForge
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Notes

This is a demo interface and does not connect to a real blockchain, wallet backend, or database. The app is intended for frontend learning and UI prototyping.

## Future Enhancements

- connect to a real backend/API
- add actual git ad
- implement wallet authentication and persistence
- add mining simulation and block validation logic
- expand into a full cryptocurrency management dashboard
