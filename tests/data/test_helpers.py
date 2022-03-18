import pandas
from datetime import datetime
from data.schema import Columns
from data.helpers import clean_data


def test_clean_data():
    data = {Columns.TXN_DATE.value: ['10/02/2022'], Columns.TXN_SHARES.value: ['1.5'], Columns.TXN_PRICE.value: ['$2.50']}
    data_frame = pandas.DataFrame(data)
    data_frame = clean_data(data_frame)
    assert data_frame[Columns.TXN_DATE.value][0] == datetime(2022, 10, 2).date()
    assert data_frame[Columns.TXN_SHARES.value][0] == 1.5
    assert data_frame[Columns.TXN_PRICE.value][0] == 2.5
