from typing import Type
from pandas import DataFrame

from cost_basis.cost_basis_calculator_factory import CostBasisCalculatorFactory, CostBasisMethod
from data.schema import Columns, TransactionType
from data.transaction import Transaction

REPORT_NAME = 'investorProfitReport'
RETURN = 'RETURN'
COST_BASES = 'COST_BASES'


class InvestorProfitReport:
    def __init__(self, cost_basis_method: CostBasisMethod, cost_basis_calculator_factory: CostBasisCalculatorFactory):
        self.cost_basis_method = cost_basis_method
        self.cost_basis_calculator_factory = cost_basis_calculator_factory
        self.cost_basis_calculators = {}
        self.investor_returns = DataFrame(
            columns=[
                Columns.INVESTOR.value,
                Columns.FUND.value,
                RETURN
            ]
        )

    def process_data(self, transaction: Transaction):
        if transaction.investor not in self.cost_basis_calculators:
            self.cost_basis_calculators[transaction.investor] = {}

        if transaction.fund not in self.cost_basis_calculators[transaction.investor]:
            self.cost_basis_calculators[transaction.investor][transaction.fund] = self.cost_basis_calculator_factory.create_cost_basis_calculator(self.cost_basis_method)

        self.process_transaction(
            transaction.investor,
            transaction.fund,
            transaction.type,
            transaction.share_count,
            transaction.price_per_share
        )

    def process_transaction(self, investor: str, fund: str, transaction_type: str, share_count: float, price_per_share: float):
        cost_basis = self.cost_basis_calculators[investor][fund].add_transaction(transaction_type, share_count, price_per_share)

        if transaction_type == TransactionType.SELL.value:
            gain_or_loss = (share_count * price_per_share) - cost_basis

            self.investor_returns = self.investor_returns.append({
                Columns.INVESTOR.value: investor,
                Columns.FUND.value: fund,
                RETURN: gain_or_loss
            }, ignore_index=True)

    def generate(self):
        self.sum_up_returns()
        self.investor_returns.to_csv(f'{REPORT_NAME}.csv')

    def sum_up_returns(self):
        self.investor_returns = self.investor_returns.groupby([Columns.INVESTOR.value, Columns.FUND.value]).sum().round(2)
