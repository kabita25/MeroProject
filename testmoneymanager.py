import unittest

from moneymanager import MoneyManager


class TestMoneyManager(unittest.TestCase):
    def setUp(self):
        # Create a test BankAccount object
        self.user = MoneyManager()

        # Provide it with some initial balance values
        self.user.balance = 1000.0

    def test_legal_deposit_works(self):
        # Your code here to test that depsositing money using the account's
        # 'deposit_funds' function adds the amount to the balance.
        self.user.deposit_funds(2000)
        self.user.deposit_funds(1000)
        print("New Balance is: ")
        print(self.user.balance)

    def test_illegal_deposit_raises_exception(self):
        # Your code here to test that depositing an illegal value (like 'bananas'
        # or such - something which is NOT a float) results in an exception being
        # raised.
        self.user.deposit_funds('banana')

    def test_legal_entry(self):
        # Your code here to test that adding a new entry with a a legal amount subtracts the
        # funds from the balance.
        self.user.add_entry(350000, "Food")
        self.user.add_entry(3000, "Rent")
        print("New Balance: ")
        print(self.user.balance)

    def test_illegal_entry_amount(self):
        # Your code here to test that withdrawing an illegal amount (like 'bananas'
        # or such - something which is NOT a float) raises a suitable exception.
        self.user.add_entry('banana', "food")

    def test_illegal_entry_type(self):
        # Your code here to test that adding an illegal entry type (like 'bananas'
        # or such - something which is NOT a float) raises a suitable exception.
        self.user.add_entry(2000, "banana")

    def test_insufficient_funds_entry(self):
        # Your code here to test that you can only spend funds which are available.
        # For example, if you have a balance of 500.00 dollars then that is the maximum
        # that can be spent. If you tried to spend 600.00 then a suitable exception
        # should be raised and the withdrawal should NOT be applied to the user balance
        # or the user's transaction list.
        self.user.add_entry(40000, "others")


# Run the unit tests in the above test case
unittest.main()
