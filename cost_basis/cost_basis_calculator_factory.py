from enum import Enum
from cost_basis.average_cost_basis_calculator import AverageCostBasisCalculator


class CostBasisMethod(Enum):
    AVERAGE_COST = 'AVERAGE-COST'
    FIFO = 'FIFO'
    LIFO = 'LIFO'
    HIFO = 'HIFO'
    LOFO = 'LOFO'


class CostBasisCalculatorFactory:
    def create_cost_basis_calculator(self, method: CostBasisMethod):
        if method == CostBasisMethod.AVERAGE_COST.value:
            return AverageCostBasisCalculator()
        elif method == CostBasisMethod.FIFO.value:
            raise NotImplementedError
        elif method == CostBasisMethod.LIFO.value:
            raise NotImplementedError
        elif method == CostBasisMethod.HIFO.value:
            raise NotImplementedError
        elif method == CostBasisMethod.LOFO.value:
            raise NotImplementedError
        else:
            raise ValueError
