"""PhysicalProduct: a Product with weight that can be shipped."""
from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A physical product: is-a Product, and realises the CanBeShipped interface."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "Fulfilment: Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """$5.00 base + $2.00 per kg."""
        return 5.00 + (2.00 * self.__weight)

    def display_information(self) -> None:
        super().display_information()
        print(f" | Type: Physical | Weight: {self.__weight}kg "
              f"| Shipping: ${self.calculate_shipping_cost():.2f} | {self.get_fulfilment_info()}")

    def to_dict(self) -> dict:
        data = self._base_dict("physical")
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["weight"])
