# import packages
import sqlite3
from simple_chalk import chalk, green
from colorama import Fore, Style

class Bank(object):
    # __init__() method - constructor method
    def __init__(self):
        self.conn = sqlite3.connect('bank.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                account_number INTEGER PRIMARY KEY,
                name TEXT,
                balance REAL
            )
            ''')
        self.conn.commit()
    
    # main functions
    # Creating account function
    def create_account(self):
        account_number = int(input('Enter account number: '))
        name = input('Enter customer name: ')
        self.cursor.execute('SELECT * FROM customers WHERE account_number =?', (account_number,))
        existing_account = self.cursor.fetchone()
        if not existing_account:
            self.cursor.execute('INSERT INTO customers VALUES (?,?,?)', (account_number, name, 0))
            self.conn.commit()
            print(chalk.green(f'Account created for {name} with account number {account_number}'))
        else:
            print(chalk.red('Account number already exists. Please choose a different account number.'))
    
    
    # Deposit Function
    def deposit(self):
        account_number = int(input('Enter account number: '))
        amount = float(input('Enter deposit amount: '))
        
        self.cursor.execute('SELECT * FROM customers WHERE account_number = ?', (account_number,))
        account = self.cursor.fetchone()
        if account:
            new_balance = account[2] + amount
            self.cursor.execute('UPDATE customers SET balance = ? WHERE account_number =?', (new_balance, account_number))
            self.conn.commit()
            print(chalk.green(f'Deposit of {amount} made to account number {account_number}'))
        else:
            print(chalk.red('Account number does not exist'))
    
    # Widthdrawing function
    def withdraw(self):
        account_number = int(input('Enter account number: '))
        amount = float(input('Enter withdrawal amount: '))
        
        self.cursor.execute('SELECT * FROM customers WHERE account_number = ?', (account_number,))
        account = self.cursor.fetchone()
        if account:
            if account[2] >= amount:
                new_balance = account[2] - amount
                self.cursor.execute('UPDATE customers SET balance = ? WHERE account_number = ?', (new_balance, account_number))
                print(chalk.green(f'Withdrawal of {amount} made from account number {account_number}'))
            else:
                print(chalk.red('Insufficient Balance!'))
        else:
            print(chalk.red('Account number does not exist'))
    
    # Checking balance function
    def check_balance(self):
        account_number = int(input('Enter account number: '))
        self.cursor.execute('SELECT * FROM customers WHERE account_number = ?', (account_number,))
        account = self.cursor.fetchone()
        if account:
            account_number, name, balance = account[0], account[1], account[2]
            print(chalk.cyan(f'Account number {account_number} (Customer: {name}) has a balance of {balance}'))
        else:
            print(chalk.red('Account number does not exist'))    
    
    # Displaying accounts function
    def display_chart(self):
        self.cursor.execute('SELECT account_number, name, balance FROM customers')
        data = self.cursor.fetchall()
        if data:
            print('===== Account Balances =====')
            print(f'{Fore.YELLOW}Account Number\tName\t\t\t Balance (USD) {Style.RESET_ALL}')
            for account_number, name, balance in data:
                print(f'{account_number}\t\t{name}\t\t\t{balance}')
        else:
            print(chalk.red('No data available to display'))  


# Create a bank instance/object from the BANK class
bank = Bank()

# Program loop
while True:
    print("====Bek Bank Menu====")
    print('1. Create Account')
    print('2. Deposit')
    print('3. Withdraw')
    print('4. Check Balance')
    print('5. Display Chart')
    print('0. Exit')
    choice = int(input('Enter your choice and hit enter >>> '))
    
    if choice == 0:
        goodbye = green.bgWhite.yellow.bgBlack
        print(goodbye('Thank you for your business, and see you soon!'))
        break
    elif choice == 1:
        bank.create_account()
          
    elif choice == 2:
        bank.deposit()
          
    elif choice == 3:
        bank.withdraw()
          
    elif choice == 4:
        bank.check_balance()
          
    elif choice == 5:
        bank.display_chart()
          
    else:
        print(chalk.red('Invalid choice. Please try again!'))
    
    
    









