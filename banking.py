import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
from datetime import datetime

# ---------- File Storage ----------
accounts_file = "accounts.json"
 
def load_accounts():
    if os.path.exists(accounts_file):
        with open(accounts_file, "r") as f:
            return json.load(f)
    return {}

def save_accounts():
    with open(accounts_file, "w") as f:
        json.dump(accounts, f, indent=4)

accounts = load_accounts()

# ---------- Core Functions ----------
def create_account():
    name = entry_name.get()
    acc_no = entry_acc.get()
    try:
        balance = float(entry_balance.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid balance amount!")
        return

    if acc_no in accounts:
        messagebox.showerror("Error", "Account already exists!")
    else:
        accounts[acc_no] = {
            "name": name,
            "balance": balance,
            "transactions": [f"[{timestamp()}] Account created with ₹{balance}"]
        }
        save_accounts()
        messagebox.showinfo("Success", f"Account created for {name}")
        clear_entries()

def deposit():
    acc_no = entry_acc.get()
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid deposit amount!")
        return

    if acc_no in accounts:
        accounts[acc_no]["balance"] += amount
        accounts[acc_no]["transactions"].append(f"[{timestamp()}] Deposited ₹{amount}")
        save_accounts()
        messagebox.showinfo("Success", f"₹{amount} deposited.")
    else:
        messagebox.showerror("Error", "Account not found.")

def withdraw():
    acc_no = entry_acc.get()
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid withdrawal amount!")
        return

    if acc_no in accounts and accounts[acc_no]["balance"] >= amount:
        accounts[acc_no]["balance"] -= amount
        accounts[acc_no]["transactions"].append(f"[{timestamp()}] Withdrew ₹{amount}")
        save_accounts()
        messagebox.showinfo("Success", f"₹{amount} withdrawn.")
    else:
        messagebox.showerror("Error", "Insufficient balance or account not found.")

def check_balance():
    acc_no = entry_acc.get()
    if acc_no in accounts:
        bal = accounts[acc_no]["balance"]
        messagebox.showinfo("Balance", f"{accounts[acc_no]['name']}'s Balance: ₹{bal}")
    else:
        messagebox.showerror("Error", "Account not found.")

def show_transaction_history():
    acc_no = entry_acc.get()
    if acc_no not in accounts:
        messagebox.showerror("Error", "Account not found.")
        return

    history_window = tk.Toplevel(root)
    history_window.title(f"Transaction History - {acc_no}")
    history_window.geometry("500x400")
    
    tk.Label(history_window, text=f"Transaction History for {accounts[acc_no]['name']}", font=("Arial", 14, "bold")).pack(pady=10)

    history_text = scrolledtext.ScrolledText(history_window, font=("Courier", 11), wrap=tk.WORD)
    history_text.pack(expand=True, fill="both", padx=10, pady=10)

    for txn in accounts[acc_no].get("transactions", []):
        history_text.insert(tk.END, txn + "\n")
    
    history_text.config(state=tk.DISABLED)

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_acc.delete(0, tk.END)
    entry_balance.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("🪙 Banking Management System")
root.geometry("530x600")
root.configure(bg="#e9f0f7")

font_label = ("Arial", 12)
font_entry = ("Arial", 12)
font_button = ("Arial", 12, "bold")

# ----- Title -----
tk.Label(root, text="Banking Management System", font=("Arial", 18, "bold"), bg="#e9f0f7", fg="#003366").pack(pady=15)

# ----- Account Creation Frame -----
frame_create = tk.LabelFrame(root, text="Create Account", font=font_label, padx=15, pady=10, bg="#f5faff")
frame_create.pack(padx=20, pady=10, fill="both")

tk.Label(frame_create, text="👤 Name:", font=font_label, bg="#f5faff").grid(row=0, column=0, sticky="e", pady=5)
entry_name = tk.Entry(frame_create, font=font_entry)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_create, text="🏦 Account No.:", font=font_label, bg="#f5faff").grid(row=1, column=0, sticky="e", pady=5)
entry_acc = tk.Entry(frame_create, font=font_entry)
entry_acc.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_create, text="💰 Opening Balance:", font=font_label, bg="#f5faff").grid(row=2, column=0, sticky="e", pady=5)
entry_balance = tk.Entry(frame_create, font=font_entry)
entry_balance.grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_create, text="➕ Create Account", command=create_account, bg="#007acc", fg="white", font=font_button).grid(row=3, columnspan=2, pady=10)

# ----- Transaction Frame -----
frame_transaction = tk.LabelFrame(root, text="Transactions", font=font_label, padx=15, pady=10, bg="#f5faff")
frame_transaction.pack(padx=20, pady=10, fill="both")

tk.Label(frame_transaction, text="💵 Amount:", font=font_label, bg="#f5faff").grid(row=0, column=0, sticky="e", pady=5)
entry_amount = tk.Entry(frame_transaction, font=font_entry)
entry_amount.grid(row=0, column=1, padx=10, pady=5)

tk.Button(frame_transaction, text="💰 Deposit", command=deposit, bg="#28a745", fg="white", font=font_button).grid(row=1, column=0, padx=5, pady=10)
tk.Button(frame_transaction, text="🧾 Withdraw", command=withdraw, bg="#f0ad4e", fg="white", font=font_button).grid(row=1, column=1, padx=5, pady=10)

# ----- Bottom Buttons -----
tk.Button(root, text="📊 Check Balance", command=check_balance, bg="#6f42c1", fg="white", font=font_button).pack(pady=8)
tk.Button(root, text="📜 Show Transaction History", command=show_transaction_history, bg="#17a2b8", fg="white", font=font_button).pack(pady=8)
tk.Button(root, text="🧹 Clear Fields", command=clear_entries, bg="#dc3545", fg="white", font=font_button).pack(pady=8)

root.mainloop()
