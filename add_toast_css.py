with open("style.css", "a") as f:
    f.write('''

/* Toast Notification System */
#toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 350px;
    width: 90%;
    pointer-events: none;
}

.toast {
    pointer-events: auto;
    background: #1e293b;
    border-left: 5px solid #00d2ff;
    color: #fff;
    padding: 14px 18px;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.9rem;
    animation: slideIn 0.3s ease-out forwards;
}

.toast.success { border-left-color: #2ecc71; }
.toast.received { border-left-color: #9b59b6; background: #2a1b3d; }
.toast.error { border-left-color: #e74c3c; }

.toast-close {
    background: none;
    border: none;
    color: #94a3b8;
    font-weight: bold;
    font-size: 1.1rem;
    cursor: pointer;
    margin-left: 10px;
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes fadeOut {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(100%); }
}
''')

print("style.css updated with toast styles!")
