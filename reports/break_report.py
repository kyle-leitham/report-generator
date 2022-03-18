from pandas import DataFrame
from data.schema import Columns, TransactionType
from data.transaction import Transaction

REPORT_NAME = 'breakReport'
CASH = 'CASH'
SHARES = 'SHARES'
ERROR = 'ERROR'
NEGATIVE_CASH_BALANCE = 'Negative cash balance'
NEGATIVE_SHARE_BALANCE_FOR = 'Negative share balance for'


class BreakReport:
    def __init__(self):
        self.investor_balances = {}
        self.errors = DataFrame(
            columns=[
                Columns.INVESTOR.value,
                ERROR
            ]
        )

    def process_data(self, transaction: Transaction):
        if transaction.investor not in self.investor_balances:
            self.investor_balances[transaction.investor] = {
                CASH: 0,
                SHARES: {}
            }

        self.process_transaction(
            transaction.investor,
            transaction.fund,
            transaction.type,
            transaction.share_count,
            transaction.get_total_transaction_amount()
        )

    def process_transaction(self, investor: str, fund: str, transaction_type: str, share_count: float, total_transaction_amount: float):
        cash_arithmetic_sign = 1 if transaction_type == TransactionType.SELL.value else -1
        shares_arithmetic_sign = -1 * cash_arithmetic_sign
        self.investor_balances[investor][CASH] += cash_arithmetic_sign * total_transaction_amount

        if fund not in self.investor_balances[investor][SHARES]:
            self.investor_balances[investor][SHARES][fund] = 0

        self.investor_balances[investor][SHARES][fund] += shares_arithmetic_sign * share_count

    def generate(self):
        self.find_erroneous_balances()
        self.errors.to_csv(f'{REPORT_NAME}.csv', index=False)

    def find_erroneous_balances(self):
        for investor in self.investor_balances:
            if self.investor_balances[investor][CASH] < 0:
                self.add_error(investor, NEGATIVE_CASH_BALANCE)

            for fund in self.investor_balances[investor][SHARES]:
                if self.investor_balances[investor][SHARES][fund] < 0:
                    self.add_error(investor, f'{NEGATIVE_SHARE_BALANCE_FOR} {fund}')

    def add_error(self, investor: str, error_message: str):
        error = {
            Columns.INVESTOR.value: investor,
            ERROR: error_message
        }

        self.errors = self.errors.append(error, ignore_index=True)