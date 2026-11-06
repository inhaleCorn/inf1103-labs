"""Order: composed of OrderLine objects that it creates and manages."""
from order_line import OrderLine
from product import Product


class Order:
    """Owns its OrderLines: it creates them, hands out only copies, and removes them with itself."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates the OrderLine internally (never passed in from outside)."""
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        """Removes the line for a product; the Product itself is untouched."""
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def cancel(self) -> None:
        """Cancelling the order removes its lines with it."""
        self.__order_lines.clear()

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")
