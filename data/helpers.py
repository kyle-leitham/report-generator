import math
from pandas import DataFrame, to_datetime
from data.schema import Columns


def clean_data(data_frame: DataFrame) -> DataFrame:
    data_frame[Columns.TXN_DATE.value] = to_datetime(data_frame[Columns.TXN_DATE.value], format="%m/%d/%Y")
    data_frame[Columns.TXN_DATE.value] = data_frame[Columns.TXN_DATE.value].dt.date
    data_frame[Columns.TXN_SHARES.value] = data_frame[Columns.TXN_SHARES.value].astype(float)
    data_frame[Columns.TXN_PRICE.value] = data_frame[Columns.TXN_PRICE.value].str.replace('$', '').astype(float)
    return data_frame


def get_quarter(month: int) -> int:
    return math.ceil(month/3)
