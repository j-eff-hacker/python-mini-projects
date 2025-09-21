# Custom Exception
class InsufficientFundsError(Exception):
    def __init__(self, value):
        self.value = value


# Base Class
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
        self.transactions = []

    # Encapsulation + Property
    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        else:
            self.__balance = value

    # Deposit
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        else:
            self.__balance += amount
            self.transactions.append(f"Deposited: {amount}")
            print(f"{amount} deposited. Balance = {self.__balance}")

    # Withdraw
    def withdraw(self, amount):
        if amount > self.__balance:
            raise InsufficientFundsError("Not enough funds!")
        else:
            self.__balance -= amount
            self.transactions.append(f"Withdrew: {amount}")
            print(f"{amount} withdrawn. Balance = {self.__balance}")

    # Magic Method
    def __str__(self):
        return f"Account({self.owner}, Balance: {self.__balance})"

    # File Handling → Save transactions
    def save_transactions(self, filename="transactions.txt"):
        with open(filename, "a") as f:
            for t in self.transactions:
                f.write(f"{self.owner}: {t}\n")
        self.transactions.clear()


# Polymorphism → Different account types
class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        if amount > self.balance - 1000:  # min balance rule
            raise InsufficientFundsError("Cannot withdraw: minimum balance rule!")
        else:
            super().withdraw(amount)


class CurrentAccount(BankAccount):
    def withdraw(self, amount):
        # Current account allows overdraft up to -5000
        if amount > self.balance + 5000:
            raise InsufficientFundsError("Overdraft limit exceeded!")
        self.balance -= amount
        self.transactions.append(f"Withdrew: {amount} (overdraft allowed)")
        print(f"{amount} withdrawn. Balance = {self.balance}")


# Demo
if __name__ == "__main__":
    try:
        acc1 = SavingsAccount("Jeffrey", 5000)
        acc1.deposit(2000)
        acc1.withdraw(1000)
        acc1.withdraw(5500)  # ❌ raises custom error
    except Exception as e:
        print("Error:", e)
    finally:
        acc1.save_transactions()
