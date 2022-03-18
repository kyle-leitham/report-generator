import numpy
from pandas import DataFrame, to_datetime
from data.schema import Columns, TransactionType, validate


def test_validate_given_valid_schema_returns_no_errors():
    data = {
        Columns.TXN_DATE.value: ['02/01/2022'],
        Columns.TXN_TYPE.value: TransactionType.BUY.value,
        Columns.TXN_SHARES.value: [1.5],
        Columns.TXN_PRICE.value: [2.5],
        Columns.FUND.value: ['fund'],
        Columns.INVESTOR.value: ['investor'],
        Columns.ADVISOR.value: ['advisor']
    }
    data_frame = DataFrame(data)

    data_frame[Columns.TXN_DATE.value] = to_datetime(data_frame[Columns.TXN_DATE.value])
    data_frame[Columns.TXN_DATE.value] = data_frame[Columns.TXN_DATE.value].dt.date
    data_frame[Columns.TXN_SHARES.value] = data_frame[Columns.TXN_SHARES.value].astype(numpy.float16)
    data_frame[Columns.TXN_PRICE.value] = data_frame[Columns.TXN_PRICE.value].astype(numpy.float16)

    validation_errors = validate(data_frame)
    assert len(validation_errors) == 0


def test_validate_given_wrong_date_format_returns_error():
    data = {
        Columns.TXN_DATE.value: ['01/02/2022'],
        Columns.TXN_TYPE.value: TransactionType.BUY.value,
        Columns.TXN_SHARES.value: [1.5],
        Columns.TXN_PRICE.value: [2.5],
        Columns.FUND.value: ['fund'],
        Columns.INVESTOR.value: ['investor'],
        Columns.ADVISOR.value: ['advisor']
    }
    data_frame = DataFrame(data)

    data_frame[Columns.TXN_SHARES.value] = data_frame[Columns.TXN_SHARES.value].astype(numpy.float16)
    data_frame[Columns.TXN_PRICE.value] = data_frame[Columns.TXN_PRICE.value].astype(numpy.float16)

    validation_errors = validate(data_frame)
    assert len(validation_errors) == 1
    assert validation_errors[0].column == Columns.TXN_DATE.value


def test_validate_given_invalid_transaction_type_returns_error():
    data = {
        Columns.TXN_DATE.value: ['02/01/2022'],
        Columns.TXN_TYPE.value: 'SOLD',
        Columns.TXN_SHARES.value: [1.5],
        Columns.TXN_PRICE.value: [2.5],
        Columns.FUND.value: ['fund'],
        Columns.INVESTOR.value: ['investor'],
        Columns.ADVISOR.value: ['advisor']
    }
    data_frame = DataFrame(data)

    data_frame[Columns.TXN_DATE.value] = to_datetime(data_frame[Columns.TXN_DATE.value])
    data_frame[Columns.TXN_DATE.value] = data_frame[Columns.TXN_DATE.value].dt.date
    data_frame[Columns.TXN_SHARES.value] = data_frame[Columns.TXN_SHARES.value].astype(numpy.float16)
    data_frame[Columns.TXN_PRICE.value] = data_frame[Columns.TXN_PRICE.value].astype(numpy.float16)

    validation_errors = validate(data_frame)
    assert len(validation_errors) == 1
    assert validation_errors[0].column == Columns.TXN_TYPE.value


def test_validate_given_missing_column_returns_error():
    data = {
        Columns.TXN_DATE.value: ['02/01/2022'],
        Columns.TXN_TYPE.value: 'SOLD',
        Columns.TXN_SHARES.value: [1.5],
        Columns.TXN_PRICE.value: [2.5],
        Columns.INVESTOR.value: ['investor'],
        Columns.ADVISOR.value: ['advisor']
    }
    data_frame = DataFrame(data)

    data_frame[Columns.TXN_DATE.value] = to_datetime(data_frame[Columns.TXN_DATE.value])
    data_frame[Columns.TXN_DATE.value] = data_frame[Columns.TXN_DATE.value].dt.date
    data_frame[Columns.TXN_SHARES.value] = data_frame[Columns.TXN_SHARES.value].astype(numpy.float16)
    data_frame[Columns.TXN_PRICE.value] = data_frame[Columns.TXN_PRICE.value].astype(numpy.float16)

    validation_errors = validate(data_frame)
    assert len(validation_errors) == 1
