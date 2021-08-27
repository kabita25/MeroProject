import tkinter as tk
from tkinter import *

import sys

from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt

from moneymanager import MoneyManager

win = tk.Tk()



# Set window size here to '540 x 640'/
win.geometry('540x640')

# Set the window title to 'FedUni Money Manager'/
Title='FedUni Money Manager'
win.title(Title)

# The user number and associated variable/
user_number_var = tk.StringVar()

# This is set as a default for ease of testing/
user_number_var.set('123456')
user_number_entry = tk.Entry(win, textvariable=user_number_var)
user_number_entry.focus_set()

# The pin number entry and associated variables/
pin_number_var = tk.StringVar()
# This is set as a default for ease of testing/
pin_number_var.set('7890')

# Modify the following to display a series of * rather than the pin ie **** not 1234/
user_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var, bd=5, width=30, show="*")





# set the user file by default to an empty string/
user_file = ''

# The balance label and associated variable/
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
# amount_var = tk.StringVar()

entry_type = tk.StringVar()
entry_type.set("Rent")
entry_type_list = {'Deposit', 'Rent','Food','Bills', 'Entertainment', 'Others'}
drop_down_list = OptionMenu(win, entry_type, *entry_type_list)

amount_var = tk.StringVar()
amount_entry = tk.Entry(win)
amount_entry = tk.Entry(win, textvariable=amount_var)
amount_entry.focus_set()

# The transaction text widget holds text of the transactions/
transaction_text_widget = tk.Text(win, height=10, width=48)

# The money manager object we will work with/
user = MoneyManager()


# ---------- Button Handlers for Login Screen ----------


def clear_pin_entry():

    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here

    user_pin_entry.delete(0, tk.END)
    user_pin_entry.insert(0, "")


def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry.'''
    # Limit to 4 chars in length
    if len(pin_number_var.get()) > 0:
        pin_number_var.set(pin_number_var.get()[:4])

    # Set the new pin number on the pin_number_var

def log_in(event):
    '''Function to log in to the banking system using a known user number and PIN.'''
    global user
    global pin_number_var
    global user_file
    global user_num_entry
    transaction_list = []

    # Create the filename from the entered account number with '.txt' on the end
    user_file = user_number_var.get() + '.txt'


    # Try to open the account file for reading
    # Open the account file for reading
    fl = open(user_file)

    # First line is account number
    acc_number = fl.readline()
    acc_number = int(acc_number.strip())

    # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
    usrpin_number = fl.readline()
    usrpin_number = int(usrpin_number.strip())

    if int(user_number_var.get()) ==acc_number and int(pin_number_var.get()) == usrpin_number:
        allowRead = 1
    else:
        print("Wrong Username or Password. Please try again.")
        clear_pin_entry(1)
        allowRead = 0

    # Read third and fourth lines (balance and interest rate)
    balance = fl.readline()
    balance = float(balance.strip())
    interest_rate = fl.readline()
    interest_rate = int(interest_rate.strip())
    # Section to read account transactions from file - start an infinite 'do-while' loop here
    while allowRead:

        # Attempt to read a line from the account file, break if we've hit the end of the file. If we
        # read a line then it's the transaction type, so read the next line which will be the transaction amount.
        line1 = fl.readline().strip()
        if line1 == '':
            break

        line2 = fl.readline().strip()
        if line2 == '':
            break

        # and then create a tuple from both lines and add it to the account's transaction_list
        tuple_both_line = line1, line2
        transaction_list.append(tuple_both_line)

    # Close the file now we're finished with it
        fl.close()
        balance_var.set('Balance: $' + str(balance))
        user.username = acc_number
        user.pin_number = usrpin_number
        user.balance = balance
        user.transaction_list = transaction_list
        print(transaction_list)

        remove_all_widgets()

        create_user_screen()

     # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    #except IOError:
      #user.__init__
    # Show error messagebox and & reset BankAccount object to default...
     #messagebox.showinfo("Error Message", "Invalid input, Please enter a valid Account Number")
      #  ...also clear PIN entry and change focus to account number entry
    #user_number_entry.delete(0, tk.END)
    #user_number_entry.insert(0, "")
    #user_number_entry.focus_set()



# Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen


# ---------- Button Handlers for User Screen ----------

def save_and_log_out():
    '''Function  to overwrite the user file with the current state of
       the user object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global user

    # Save the account with any new transactions
    user.save_to_file()

    # Reset the bank acount object
    user = MoneyManager()
    # Reset the account number and pin to blank
    clear_pin_entry(1)
    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()

    user_pin_entry.delete(0, tk.END)
    user_pin_entry.insert(0, "")

    user_number_entry.delete(0, tk.END)
    user_number_entry.insert(0, "")
    user_number_entry.focus_set()

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       user's transaction list.'''
    global user
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file

    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        user.balance = user.deposit_funds(amount_entry.get())
        # Deposit funds
        deposit_amount = float(amount_entry.get())

        user.amount_entry = deposit_amount
        user.transaction_type = 'Deposit'
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        transaction_datas = user.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.config(state='normal')
        transaction_text_widget.delete('1.0', tk.END)
        transaction_text_widget.insert('1.0', "")
        for transaction_data in transaction_datas:
            transaction_text_widget.insert(tk.END, transaction_data[0])
            transaction_text_widget.insert(tk.END, '\n')
            transaction_text_widget.insert(tk.END, transaction_data[1])
            transaction_text_widget.insert(tk.END, '\n')

        # Change the balance label to reflect the new balance
        balance = 'Balance: $ ' + str(user.balance)
        balance_var.set(balance)
        # Clear the amount entry
        user.amount_entry = 0.0
        # Update the interest graph with our new balance
        plot_spending_graph()
        # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except IOError as showerror:
        messagebox.showinfo("Transaction Error", showerror)

def perform_transaction():
    '''Function to add the entry the amount in the amount entry from the user balance and add an entry to the transaction list.'''
    global user
    global amount_entry
    global balance_label
    global balance_var
    global entry_type

    # Try to decrease the account balance and append the deposit to the account file
    # Get the cash amount to use. Note: We check legality inside account's withdraw_funds method

    try:
        # Get the cash amount to use. Note: We check legality inside account's withdraw_funds method
        deposit = amount_var.get()

        # Get the type of entry that will be added ie rent etc
        transaction_type = entry_type.get()

        # Withdraw funds from the balance
        user.add_entry(deposit, transaction_type)

        # Update the transaction widget with the new transaction by calling user.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        user.get_transaction_string()
        transaction_text_widget.config(state=NORMAL)
        transaction_text_widget.delete(1.0, END)
        transaction_text_widget.insert(END, user.transacation_string)
        transaction_text_widget.config(state=DISABLED)

        # Change the balance label to reflect the new balance
        balance_var.set('Balance: $' + str(user.balance))

        # Clear the amount entry
        amount_var.set("")

        # Update the graph

    # Catch and display any returned exception as a messagebox 'showerror'
    except Exception as error:
        messagebox.showerror("Error:", repr(error))
        print('Error: ' + repr(error))




def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()


def read_line_from_user_file():
    '''Function to read a line from the users file but not the last newline character.
       Note: The user_file must be open to read from for this function to succeed.'''
    global user_file
    return user_file.readline()[0:-1]


def plot_spending_graph():
    x_list = []
    y_list = []
    # YOUR CODE to generate the x and y lists here which will be plotted
    for transactions in user.transaction_list:
        x_list.append(transactions[0])
        y_list.append(transactions[1])

    # Your code to display the graph on the screen here - do this last
    figure = Figure(figsize=(4, 2), dpi=102)
    figure.suptitle('Transactions Histogam')
    histogram = figure.add_subplot(111)
    histogram.hist(y_list, rwidth=0.90)
    histogram.grid()

    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=5, column=0, columnspan=4, sticky='nsew')


# ---------- UI Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''

    # ----- Row 0 -----

    # 'FedUni Money Manager' label here. Font size is 28.
    thelabel=tk.Label(win, text=Title, font=("Trajan", 28))
    thelabel.grid(row=0, column=0, columnspan=3, stick="nsew")



    # ----- Row 1 -----

    # Acount Number / Pin label here
    tk.Label(win, text="Account Number").grid(row=1, column=0, stick="nsew")

    # Pin number entry label here
    #tk.Label(win, text="Pin Code").grid(row=1, column=1, stick="nsew")

    # Account number entry here
    user_number_entry.grid(row=1, column=1, sticky="nsew")



    # Account pin entry here
    user_pin_entry.grid(row=1,column=2,sticky='nsew')


    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn1 = Button(win, text=' 1 ', command=lambda *args: handle_pin_button(1))
    btn1.grid(row=2, column=0, stick='nsew')

    btn2 = Button(win, text=' 2 ', command=lambda *args: handle_pin_button(2))
    btn2.grid(row=2, column=1, stick='nsew')

    btn3 = Button(win, text=' 3 ', command=lambda *args: handle_pin_button(3))
    btn3.grid(row=2, column=2, stick='nsew')

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn4 = Button(win, text=' 4 ', command=lambda *args: handle_pin_button(4))
    btn4.grid(row=3, column=0, stick='nsew')

    btn5 = Button(win, text=' 5 ', command=lambda *args: handle_pin_button(5))
    btn5.grid(row=3, column=1, stick='nsew')

    btn6 = Button(win, text=' 6 ', command=lambda *args: handle_pin_button(6))
    btn6.grid(row=3, column=2, stick='nsew')

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn7 = Button(win, text=' 7 ', command=lambda *args: handle_pin_button(7))
    btn7.grid(row=4, column=0, stick='nsew')

    btn8 = Button(win, text=' 8 ', command=lambda *args: handle_pin_button(8))
    btn8.grid(row=4, column=1, stick='nsew')

    btn9 = Button(win, text=' 9 ', command=lambda *args: handle_pin_button(9))
    btn9.grid(row=4, column=2, stick='nsew')

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    btn10 = tk.Button(win, text=' Cancel/Clear ', fg='black', bg='red', command=clear_pin_entry)
    btn10.grid(row=5, column=0, stick='nsew')

    # Button 0 here

    btn0 = Button(win, text=' 0 ', command=lambda *args: handle_pin_button(0))
    btn0.grid(row=5, column=1, stick='nsew')

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    btn_login = tk.Button(win, text="Login", command=log_in, bg='green')
    btn_login.grid(row=5, column=2, sticky='nsew')

    # ----- Set column & row weights -----
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)

    win.rowconfigure(0, weight=2)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=2)
    win.rowconfigure(3, weight=2)
    win.rowconfigure(4, weight=2)
    win.rowconfigure(5, weight=2)

    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)

    #win.columnconfigure(3, weight=1)


def create_user_screen():
    '''Function to create the user screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var

    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    Hlabel = tk.Label(win, text="Title", font=("Tarjan", 24))
    Hlabel.grid(row=0, column=0, columnspan=5, sticky='nsew')


    # ----- Row 1 -----

    # Account number label here
    tk.Label(win, text=" User Account Number: " + user_number_var.get()).grid(row=1, column=0, stick="nsew")

    # Balance label here
    balance_label.grid(row=1, column=1, stick="nsew")

    # Log out button here
    signout_btn = Button(win, text=' Sign Out ', command=lambda: save_and_log_out())
    signout_btn.grid(row=1, column=2, stick="nsew")

    # ----- Row 2 -----

    # Amount label here
    tk.Label(win, text=" Amount ").grid(row=2, column=0, stick="nsew")
    # Amount entry here
    amount_entry.grid(row=2, column=1, stick="nsew")
    # Deposit button here
    deposit_btn = Button(win, text=' Deposit ', command=lambda: perform_deposit())
    deposit_btn.grid(row=2, column=2, stick="nsew")

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.

    # ----- Row 3 -----
    # Entry type label here
    tk.Label(win, text=" Entry Type ").grid(row=3, column=0, stick="nsew")

    # Entry drop list here
    drop_down_list.grid(row=3, column=1, stick="nsew")

    # Add entry button here
    add_entry_btn = Button(win, text=' Add Next Entry ', command=lambda: perform_transaction())
    add_entry_btn.grid(row=3, column=2, stick="nsew")

    # ----- Row 4 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    text_scrollbar = tk.Scrollbar(win)

    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited


    transaction_text_widget.grid(row=4, column=0, columnspan=5, sticky='NSEW')
    for transaction_data in user.transaction_list:
        transaction_text_widget.insert(tk.END, transaction_data[0])
        transaction_text_widget.insert(tk.END, '\n')
        transaction_text_widget.insert(tk.END, transaction_data[1])
        transaction_text_widget.insert(tk.END, '\n')
    transaction_text_widget.config(state='disabled')
    # Now add the scrollbar and set it to change with the yview of the text widget
    transaction_text_widget.config(yscrollcommand=text_scrollbar.set)
    text_scrollbar.config(command=transaction_text_widget.yview)
    text_scrollbar.grid(row=4, column=5, sticky='nsew')

    # ----- Row 5 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_intrst_graph_btn = Button(win, text='Plot the Graph', command=lambda: plot_spending_graph())
    plot_intrst_graph_btn.grid(row=5, column=2, stick="nsew")

    # ----- Set column & row weights -----
    win.rowconfigure(0, weight=2)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=2)
    win.rowconfigure(4, weight=2)
    win.rowconfigure(5, weight=2)

    win.columnconfigure(0, weight=2)
    win.columnconfigure(1, weight=2)
    win.columnconfigure(2, weight=2)


    # Set column and row weights here - there are 6 rows and 5 columns (numbered 0 through 4 not 1 through 5!)



# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
