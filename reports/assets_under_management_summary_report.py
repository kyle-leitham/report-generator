from pandas import DataFrame
from data.schema import Columns, TransactionType
from data.transaction import Transaction

REPORT_NAME = 'assetsUnderManagementSummaryReport'
ASSET_UNDER_MANAGEMENT = 'ASSETS_UNDER_MANAGEMENT'


class AssetsUnderManagementSummaryReport:
    def __init__(self):
        self.fund_prices = {}
        self.advisor_assets = {}
        self.assets_under_management = DataFrame(
            columns=[
                Columns.ADVISOR.value,
                ASSET_UNDER_MANAGEMENT
            ]
        )

    def process_data(self, transaction: Transaction):
        if transaction.advisor not in self.advisor_assets:
            self.advisor_assets[transaction.advisor] = {}

        self.process_transaction(
            transaction.advisor,
            transaction.fund,
            transaction.type,
            transaction.share_count,
            transaction.price_per_share
        )

    def process_transaction(self, advisor: str, fund: str, transaction_type: str, share_count: float, price_per_share: float):
        self.fund_prices[fund] = price_per_share

        if fund not in self.advisor_assets[advisor]:
            self.advisor_assets[advisor][fund] = 0

        arithmetic_sign = 1 if transaction_type == TransactionType.BUY.value else -1
        self.advisor_assets[advisor][fund] += arithmetic_sign * share_count

    def generate(self):
        self.calculate_assets_under_management()
        self.assets_under_management.to_csv(f'{REPORT_NAME}.csv', index=False)

    def calculate_assets_under_management(self):
        for advisor in self.advisor_assets:
            total_asset_value = 0
            for fund in self.advisor_assets[advisor]:
                total_asset_value += self.advisor_assets[advisor][fund] * self.fund_prices[fund]

            self.assets_under_management = self.assets_under_management.append({
                Columns.ADVISOR.value: advisor,
                ASSET_UNDER_MANAGEMENT: round(total_asset_value, 2)
            }, ignore_index=True)
