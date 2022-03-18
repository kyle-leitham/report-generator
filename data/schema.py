import numpy
from typing import List

from pandas import DataFrame
from pandas_schema import Schema, Column, ValidationWarning
from pandas_schema.validation import InListValidation, DateFormatValidation, IsDtypeValidation
from enum import Enum


class Columns(Enum):
    TXN_DATE = 'TXN_DATE'
    TXN_TYPE = 'TXN_TYPE'
    TXN_SHARES = 'TXN_SHARES'
    TXN_PRICE = 'TXN_PRICE'
    FUND = 'FUND'
    INVESTOR = 'INVESTOR'
    ADVISOR = 'ADVISOR'


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"


schema = Schema([
    Column(Columns.TXN_DATE.value, [DateFormatValidation('%Y-%m-%d')]),
    Column(Columns.TXN_TYPE.value, [InListValidation([transaction_type.value for transaction_type in list(TransactionType)])]),
    Column(Columns.TXN_SHARES.value),
    Column(Columns.TXN_PRICE.value),
    Column(Columns.FUND.value),
    Column(Columns.INVESTOR.value),
    Column(Columns.ADVISOR.value)
])


def validate(data_frame: DataFrame) -> List[ValidationWarning]:
    return schema.validate(data_frame)


