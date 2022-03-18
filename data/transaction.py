from collections import namedtuple
from datetime import date
from data.schema import Columns, TransactionType

TransactionTuple = namedtuple(
    'TransactionTuple',
    f'''{Columns.TXN_DATE.value}
        {Columns.TXN_TYPE.value}
        {Columns.TXN_SHARES.value}
        {Columns.TXN_PRICE.value}
        {Columns.FUND.value}
        {Columns.INVESTOR.value}
        {Columns.ADVISOR.value}'''
)


class Transaction:
    def __init__(self, data: tuple):
        self.date: date = getattr(data, Columns.TXN_DATE.value)
        self.type: TransactionType = getattr(data, Columns.TXN_TYPE.value)
        self.share_count: float = getattr(data, Columns.TXN_SHARES.value)
        self.price_per_share: float = getattr(data, Columns.TXN_PRICE.value)
        self.fund: str = getattr(data, Columns.FUND.value)
        self.investor: str = getattr(data, Columns.INVESTOR.value)
        self.advisor: str = getattr(data, Columns.ADVISOR.value)

    def get_total_transaction_amount(self) -> float:
        return self.share_count * self.price_per_share
