"""OrderLine: one product + quantity inside an Order (part of a composition)."""
from product import Product


class OrderLine:
    """References a Product (association) but does not own it. Created only by Order."""

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"  {self.__product.get_name()} x{self.__quantity} @ ${self.__product.get_price():.2f} "
              f"= ${self.calculate_subtotal():.2f}")
