"""Inventory: aggregates Product objects (products can exist outside it)."""
from product import Product


class Inventory:
    """Manages a collection of Product references. Works only with the Product abstraction."""

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Adds an existing Product; returns False if the ID is already present."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Removes the reference (the Product itself is NOT destroyed) and returns it, or None."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Returns the matching Product, or None if it cannot be found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        """Polymorphically asks every Product to display itself."""
        print("\nCurrent Inventory")
        print("-" * 80)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 80)

    def get_all_products(self) -> list[Product]:
        """Returns a copy of the product list."""
        return list(self.__products)
