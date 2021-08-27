from tkinter import messagebox

class MoneyManager():
    transaction_string = ""
    tuple_both_line = ()

    def __init__(self, username='', usrpin_number="", balance=0.0, transaction_list=[]):
        '''Constructor to set username to '', pin_number to an empty string,
           balance to 0.0, and transaction_list to an empty list.'''
        self.username = username
        self.pin_number = usrpin_number
        self.balance = balance
        self.transaction_list = transaction_list

    def add_entry(self, amount, entry_type):
        '''Function to add and entry an amount to the tool. Raises an
           exception if it receives a value for amount that cannot be cast to float. Raises an exception
           if the entry_type is not valid - i.e. not food, rent, bills, entertainment or other'''
        types = ["Food", "Rent", "Bills", "Entertainment", "Others"]
        try:
            amount = float(amount)
            if entry_type in types:
                difference = self.balance - amount
            else:
                raise Exception('Entry Type not valid')
            if (difference < 0):
                raise Exception('You have no balance in your account.')
            else:
                self.balance = difference
                tuple_both_line = str(entry_type), str(amount)
                self.transaction_list.append(tuple_both_line)
        except ValueError:
            messagebox.showerror("Value Error", "Not a valid value")
            print("Not a valid value")
        except Exception as error:
            messagebox.showerror("Error", 'Caught this error: ' + repr(error))
            print('Caught this error: ' + repr(error))

    def deposit_funds(self, amount):
        '''Function to deposit an amount to the user balance. Raises an
           exception if it receives a value that cannot be cast to float. '''
        try:
            amount = float(amount)
            self.balance += amount
            tuple_both_line = "Deposit", str(amount)
            self.transaction_list.append(tuple_both_line)
        except ValueError:
            messagebox.showerror("Value Error", "Not a valid value")
            print("Not valid.")

    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or the entry type - food etc - on
           the first line, and then the amount deposited or entry amount on the next line.'''
        transaction_string = ""
        for transaction in self.transaction_list:
            transaction_string = transaction_string + transaction[0] + "\n"
            transaction_string = transaction_string + transaction[1] + "\n"
        self.transaction_string = transaction_string

    def save_to_file(self):
        '''Function to overwrite the user text file with the current user
           details. user number, pin number, and balance (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        user_file = str(self.username) + ".txt"
        self.get_transaction_string()
        with open(user_file, 'w') as filetowrite:
            filetowrite.write(str(self.username) + '\n')
            filetowrite.write(str(self.usrpin_number) + '\n')
            filetowrite.write(str(self.balance) + '\n')
            filetowrite.write('10' + '\n')
            filetowrite.write(self.transaction_string)
            filetowrite.close()
