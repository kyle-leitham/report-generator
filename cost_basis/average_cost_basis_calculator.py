from data.schema import TransactionType


class AverageCostBasisCalculator:
    def __init__(self):
        self.total_cost = 0.0
        self.total_shares = 0.0

    def add_transaction(self, transaction_type: str, share_count: float, price_per_share: float):
        if transaction_type == TransactionType.BUY.value:
            self.total_cost += share_count * price_per_share
            self.total_shares += share_count
            return 0
        else:
            cost_basis = (self.total_cost / self.total_shares) * share_count
            self.total_cost -= cost_basis
            self.total_shares -= share_count
            return cost_basis
