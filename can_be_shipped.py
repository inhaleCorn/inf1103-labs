"""Interface-style abstract base class: the contract for anything that can be shipped."""
from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Contract for items that require shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns the shipping cost."""
        pass
