from cost_basis.average_cost_basis_calculator import AverageCostBasisCalculator
from data.schema import TransactionType


def test_add_transaction():
    average_cost_basis_calculator = AverageCostBasisCalculator()
    average_cost_basis_calculator.add_transaction(TransactionType.BUY.value, 1.0, 2.0)
    average_cost_basis_calculator.add_transaction(TransactionType.BUY.value, 3.0, 10.0)
    cost_basis = average_cost_basis_calculator.add_transaction(TransactionType.SELL.value, 2.0, 15.0)
    assert cost_basis == 16


def test_add_transaction_with_two_sales():
    average_cost_basis_calculator = AverageCostBasisCalculator()
    average_cost_basis_calculator.add_transaction(TransactionType.BUY.value, 1.0, 2.0)
    average_cost_basis_calculator.add_transaction(TransactionType.BUY.value, 3.0, 10.0)
    average_cost_basis_calculator.add_transaction(TransactionType.SELL.value, 2.0, 15.0)
    average_cost_basis_calculator.add_transaction(TransactionType.BUY.value, 2.0, 16.0)
    cost_basis = average_cost_basis_calculator.add_transaction(TransactionType.SELL.value, 2.0, 20.0)
    assert cost_basis == 24
