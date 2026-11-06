"""Abstract Product base class."""
from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class representing an individual product.

    A Product holds a reference to its Supplier (association): the Supplier is
    created independently and passed in, so neither owns the other.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, new_stock: int) -> None:
        """Updates the stock quantity (same meaning for every subclass - LSP)."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = new_stock

    def display_information(self) -> None:
        """Displays base product details (subclasses extend this via super())."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} "
              f"| Stock: {self.__stock} | Supplier: {self.__supplier.get_name()}", end="")

    def _base_dict(self, product_type: str) -> dict:
        """Common fields for JSON persistence, reused by subclasses."""
        return {
            "type": product_type,
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Returns product fulfilment details."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts the product to a dictionary for JSON persistence."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "Product":
        """Creates a product from dictionary data and its Supplier."""
        pass
