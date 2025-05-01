import sqlite3

conn = sqlite3.connect("bank_app.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS ACCOUNTS(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        balance REAL NOT NULL,
        acc_no NOT NULL UNIQUE

    )
"""
)


def list_accounts():

    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    if not accounts:
        print("No accounts found.")
        return

    print(
        "\n{:<5} {:<20} {:<15} {:<15}".format(
            "ID", "Name", "Balance ($)", "Account No."
        )
    )
    print("-" * 60)

    for account in accounts:
        id_, name, balance, acc_no = account
        print("{:<5} {:<20} {:<15.2f} {:<15}".format(id_, name, balance, acc_no))


def create_account(name, balance, acc_no):

    try:
        cursor.execute(
            "INSERT INTO accounts (name, balance, acc_no) VALUES (?, ?, ?)",
            (name, balance, acc_no),
        )

        conn.commit()
        print(f"\nAccount created successfully for Name: {name} (Account No: {acc_no})")
    except sqlite3.IntegrityError:
        print(
            f"\nError: Account No '{acc_no}' already exists. Please use a unique account number."
        )


def update_account(acc_no, name, balance):

    cursor.execute(
        "UPDATE accounts SET name = ?, balance = ? WHERE acc_no = ?",
        (name, balance, acc_no),
    )
    conn.commit()
    print(f"\nAccount update successfully for {name} (Account No: {acc_no})")


def delete_account(acc_no):

    cursor.execute("DELETE FROM accounts WHERE acc_no = ?", (acc_no,))
    conn.commit()
    print(f"\nAccount delete successfully for  (Account No: {acc_no})")


def main():
    while True:

        print("\nBank Account Manager App with DB")
        print("1. List Accounts")
        print("2. Create Account")
        print("3. Update Account")
        print("4. Delete Account")
        print("5. Exit App")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_accounts()

        elif choice == "2":

            try:
                name = input("Enter account holder name: ")
                acc_no = int(input("Enter account no. : "))
                balance = float(input("Enter initial balance: $ "))
                create_account(name, balance, acc_no)
            except ValueError:
                print("Invalid input! Please enter numeric value for balance.")

        elif choice == "3":

            try:
                acc_no = int(input("Enter the account No.: "))
                name = input("Enter new account holder name: ")
                balance = float(input("Enter new balance: $ "))
                update_account(acc_no, name, balance)
            except ValueError:
                print("Invalid input! Please enter numeric value for balance.")

        elif choice == "4":

            acc_no = int(input("Enter the account no. to delete: "))
            delete_account(acc_no)

        elif choice == "5":
            break

        else:
            print("Invalid choice!")

    conn.close()


if __name__ == "__main__":
    main()
