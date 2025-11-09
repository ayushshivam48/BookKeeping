import datetime
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass, field

# --- 1. Define Account Types ---
class AccountType(Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"

    def get_balance_type(self):
        """Returns 'debit' for Asset/Expense, else 'credit'."""
        if self in {AccountType.ASSET, AccountType.EXPENSE}:
            return 'debit'
        else:
            return 'credit'

# --- 2. Account Class ---
@dataclass
class Account:
    account_id: int
    name: str
    account_type: AccountType
    balance: Decimal = Decimal('0.00')

    def increase(self, amount: Decimal):
        if self.account_type.get_balance_type() == 'debit':
            self.balance += amount
        else:
            self.balance -= amount

    def decrease(self, amount: Decimal):
        if self.account_type.get_balance_type() == 'debit':
            self.balance -= amount
        else:
            self.balance += amount

# --- 3. Transactions Classes ---
@dataclass
class Posting:
    account: Account
    amount: Decimal
    is_debit: bool

@dataclass
class JournalEntry:
    date: datetime.date
    description: str
    postings: list[Posting] = field(default_factory=list)

    def add_posting(self, account: Account, amount: Decimal, is_debit: bool):
        self.postings.append(Posting(account, amount, is_debit))

    def validate(self) -> bool:
        total_debits = sum(p.amount for p in self.postings if p.is_debit)
        total_credits = sum(p.amount for p in self.postings if not p.is_debit)
        return total_debits.quantize(Decimal('0.01')) == total_credits.quantize(Decimal('0.01'))

# --- 4. Ledger Class ---
class Ledger:
    def __init__(self):
        self.chart_of_accounts: dict[int, Account] = {}
        self.journal_entries: list[JournalEntry] = []

    def add_account(self, account_id: int, name: str, account_type: AccountType):
        if account_id in self.chart_of_accounts:
            raise ValueError(f"Account ID {account_id} already exists.")
        account = Account(account_id, name, account_type)
        self.chart_of_accounts[account_id] = account

    def add_journal_entry(self, entry: JournalEntry) -> bool:
        if not entry.validate():
            return False
        # Post debits and credits
        for posting in entry.postings:
            account = posting.account
            if posting.is_debit:
                if account.account_type.get_balance_type() == 'debit':
                    account.increase(posting.amount)
                else:
                    account.decrease(posting.amount)
            else: # Credit posting
                if account.account_type.get_balance_type() == 'credit':
                    account.increase(posting.amount)
                else:
                    account.decrease(posting.amount)
        self.journal_entries.append(entry)
        return True

    def get_account_by_id(self, account_id: int) -> Account:
        if account_id not in self.chart_of_accounts:
            raise ValueError(f"Account ID {account_id} not found.")
        return self.chart_of_accounts[account_id]