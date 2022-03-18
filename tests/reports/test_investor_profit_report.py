from pandas import DataFrame, MultiIndex
from pandas.testing import assert_frame_equal
from datetime import datetime
from cost_basis.average_cost_basis_calculator import AverageCostBasisCalculator
from cost_basis.cost_basis_calculator_factory import CostBasisMethod, CostBasisCalculatorFactory
from data.schema import TransactionType, Columns
from data.transaction import Transaction, TransactionTuple
from reports.investor_profit_report import InvestorProfitReport, RETURN


def test_given_no_sell_then_no_return_on_investment_calculated():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    investor_profit_report = InvestorProfitReport(CostBasisMethod.AVERAGE_COST.value, CostBasisCalculatorFactory())
    investor_profit_report.process_data(transaction)
    investor_profit_report.sum_up_returns()

    assert len(investor_profit_report.investor_returns) == 0


def test_given_sell_at_higher_price_positive_return_calculated():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            4.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    investor_profit_report = InvestorProfitReport(CostBasisMethod.AVERAGE_COST.value, CostBasisCalculatorFactory())
    investor_profit_report.process_data(transaction1)
    investor_profit_report.process_data(transaction2)
    investor_profit_report.sum_up_returns()

    index = MultiIndex.from_tuples([('Investor', 'Test Fund')], names=[Columns.INVESTOR.value, Columns.FUND.value])
    expected_df = DataFrame({
        RETURN: [20.00]
    }, index=index)

    assert_frame_equal(investor_profit_report.investor_returns, expected_df)


def test_given_sell_at_lower_price_negative_return_calculated():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            1.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    investor_profit_report = InvestorProfitReport(CostBasisMethod.AVERAGE_COST.value, CostBasisCalculatorFactory())
    investor_profit_report.process_data(transaction1)
    investor_profit_report.process_data(transaction2)
    investor_profit_report.sum_up_returns()

    index = MultiIndex.from_tuples([('Investor', 'Test Fund')], names=[Columns.INVESTOR.value, Columns.FUND.value])
    expected_df = DataFrame({
        RETURN: [-10.00]
    }, index=index)

    assert_frame_equal(investor_profit_report.investor_returns, expected_df)


def test_given_multiple_buys_and_sell_then_return_calculated_with_cost_basis():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            1.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            5.00,
            4.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    transaction3 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            5.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    investor_profit_report = InvestorProfitReport(CostBasisMethod.AVERAGE_COST.value, CostBasisCalculatorFactory())
    investor_profit_report.process_data(transaction1)
    investor_profit_report.process_data(transaction2)
    investor_profit_report.process_data(transaction3)
    investor_profit_report.sum_up_returns()

    index = MultiIndex.from_tuples([('Investor', 'Test Fund')], names=[Columns.INVESTOR.value, Columns.FUND.value])
    expected_df = DataFrame({
        RETURN: [30.00]
    }, index=index)

    assert_frame_equal(investor_profit_report.investor_returns, expected_df)


def test_given_two_investors_sell_then_records_for_each():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor1',
            'Advisor'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            7.00,
            'Test Fund',
            'Investor1',
            'Advisor'
        )
    )

    transaction3 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            4.00,
            'Test Fund',
            'Investor2',
            'Advisor'
        )
    )

    transaction4 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            5.00,
            'Test Fund',
            'Investor2',
            'Advisor'
        )
    )

    investor_profit_report = InvestorProfitReport(CostBasisMethod.AVERAGE_COST.value, CostBasisCalculatorFactory())
    investor_profit_report.process_data(transaction1)
    investor_profit_report.process_data(transaction2)
    investor_profit_report.process_data(transaction3)
    investor_profit_report.process_data(transaction4)
    investor_profit_report.sum_up_returns()

    index = MultiIndex.from_tuples([('Investor1', 'Test Fund'), ('Investor2', 'Test Fund')], names=[Columns.INVESTOR.value, Columns.FUND.value])
    expected_df = DataFrame({
        RETURN: [50.00, 10.00]
    }, index=index)

    assert_frame_equal(investor_profit_report.investor_returns, expected_df)


def test_given_investor_sells_two_funds_then_records_for_each():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            2.00,
            'Test Fund1',
            'Investor',
            'Advisor'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            7.00,
            'Test Fund1',
            'Investor',
            'Advisor'
        )
    )

    transaction3 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            4.00,
            'Test Fund2',
            'Investor',
            'Advisor'
        )
    )

    transaction4 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            5.00,
            'Test Fund2',
            'Investor',
            'Advisor'
        )
    )

    investor_profit_report = InvestorProfitReport(CostBasisMethod.AVERAGE_COST.value, CostBasisCalculatorFactory())
    investor_profit_report.process_data(transaction1)
    investor_profit_report.process_data(transaction2)
    investor_profit_report.process_data(transaction3)
    investor_profit_report.process_data(transaction4)
    investor_profit_report.sum_up_returns()

    index = MultiIndex.from_tuples([('Investor', 'Test Fund1'), ('Investor', 'Test Fund2')], names=[Columns.INVESTOR.value, Columns.FUND.value])
    expected_df = DataFrame({
        RETURN: [50.00, 10.00]
    }, index=index)

    assert_frame_equal(investor_profit_report.investor_returns, expected_df)