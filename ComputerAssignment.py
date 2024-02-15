from datetime import datetime

# Load existing account data from a file
def load_accounts():
    try:
        with open("accounts.txt", "r", encoding="utf-8") as file:
            accounts = {}
            for line in file:
                account_data = line.strip().split(",")
                if len(account_data) >= 3:
                    name = account_data[0]
                    password = account_data[1]
                    pin = account_data[2]
                    balance = float(account_data[3])
                    transactions = []
                    if len(account_data) > 4:
                        try:
                            transactions = eval(",".join(account_data[4:]))
                        except Exception as e:
                            print(f"Error loading transactions for {name}: {e}")
                    accounts[name] = {"password": password, "pin": pin, "balance": balance, "transactions": transactions}
        return accounts
    except FileNotFoundError:
        return {}


# Save account data to a file
def save_accounts(accounts):
    with open("accounts.txt", "w", encoding="utf-8") as file:
        for name, data in accounts.items():
            password = data["password"]
            pin = data["pin"]
            balance = data["balance"]
            transactions = data["transactions"]
            encoded_transactions = [transaction.encode("utf-8").decode("utf-8") for transaction in transactions]
            file.write(f"{name},{password},{pin},{balance},{encoded_transactions}\n")


# Main program
accounts = load_accounts()

while True:
    print("\n===== Welcome to the Banking System =====")
    print("1. Create an account")
    print("2. Access an existing account")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter your name: ")
        if name not in accounts:
            password = input("Set your password: ")
            pin = input("Set your PIN: ")
            accounts[name] = {"password": password, "pin": pin, "balance": 0, "credit": 0, "transactions": []}
            save_accounts(accounts)
            print(f"Account created for {name}.")
        else:
            print("Account with that name already exists.")
    elif choice == "2":
        name = input("Enter your name: ")
        if name in accounts:
            password = input("Enter your password: ")
            if password == accounts[name]["password"]:
                while True:
                    print("\n===== Account Menu =====")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. View Transaction History")
                    print("5. Transfer Funds")
                    print("6. Exit")

                    if accounts[name]["balance"] < 0:
                        print("ALERT: You have an outstanding credit balance. Please repay the amount.")

                    action = input("Enter your choice: ")

                    if action == "1":
                        print(f"Current balance for {name}: ₹{accounts[name]['balance']}")
                    elif action == "2":
                        amount = float(input("Enter the amount to deposit: "))
                        note = input("Enter a note (optional): ")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        accounts[name]["balance"] += amount
                        if accounts[name]["balance"] >= 0:
                            accounts[name]["credit"] = 0
                        transaction = f"{timestamp} - Deposit: ₹{amount}{' - ' + note if note else ''}"
                        accounts[name]["transactions"].append(transaction)
                        save_accounts(accounts)
                        print(f"Deposit of ₹{amount} successful. Current balance: ₹{accounts[name]['balance']}")
                    elif action == "3":
                        pin = input("Enter your PIN to proceed with withdrawal: ")
                        if pin == accounts[name]["pin"]:
                            amount = float(input("Enter the amount to withdraw: "))
                            note = input("Enter a note (optional): ")
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            if amount <= accounts[name]["balance"] + 10000:
                                accounts[name]["balance"] -= amount
                                if accounts[name]["balance"] < 0:
                                    accounts[name]["credit"] = -accounts[name]["balance"]
                                transaction = f"{timestamp} - Withdrawal: ₹{amount}{' - ' + note if note else ''}"
                                accounts[name]["transactions"].append(transaction)
                                save_accounts(accounts)
                                print(f"Withdrawal of ₹{amount} successful. Current balance: ₹{accounts[name]['balance']}")
                            else:
                                print("Exceeds credit limit. You cannot withdraw beyond ₹10,000 credit.")
                        else:
                            print("Incorrect PIN.")
                    elif action == "4":
                        print(f"Transaction History for {name}:")
                        if not accounts[name]["transactions"]:
                            print("Transaction history is empty.")
                        else:
                            for transaction in accounts[name]["transactions"]:
                                print(transaction)
                    elif action == "5":
                        pin = input("Enter your PIN to proceed with transfer: ")
                        if pin == accounts[name]["pin"]:
                            recipient_name = input("Enter recipient's name: ")
                            if recipient_name in accounts:
                                amount = float(input("Enter the amount to transfer: "))
                                note = input("Enter a note (optional): ")
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                if amount <= accounts[name]["balance"] + 10000:
                                    accounts[name]["balance"] -= amount
                                    if accounts[name]["balance"] < 0:
                                        accounts[name]["credit"] = -accounts[name]["balance"]
                                    transaction_out = f"{timestamp} - Transfer: ₹{amount} to {recipient_name}{' - ' + note if note else ''}"
                                    accounts[name]["transactions"].append(transaction_out)
                                    transaction_in = f"{timestamp} - Transfer: ₹{amount} from {name}{' - ' + note if note else ''}"
                                    accounts[recipient_name]["transactions"].append(transaction_in)
                                    accounts[recipient_name]["balance"] += amount
                                    save_accounts(accounts)
                                    print(f"₹{amount} transferred to {recipient_name}.")
                                else:
                                    print("Exceeds credit limit. You cannot transfer beyond ₹10,000 credit.")
                            else:
                                print("Recipient account not found.")
                        else:
                            print("Incorrect PIN.")
                    elif action == "6":
                        break
                    else:
                        print("Invalid choice!")
            else:
                print("Incorrect password.")
        else:
            print("Account not found.")
    elif choice == "3":
        print("Thank you for using our Banking System. Goodbye!")
        break
    else:
        print("Invalid choice!")
