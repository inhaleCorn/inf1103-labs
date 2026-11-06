"""DigitalProduct: a Product delivered online with a download size."""
from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A digital product. Not shippable, so it does not implement CanBeShipped."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Fulfilment: Delivered digitally via download link."

    def display_information(self) -> None:
        super().display_information()
        print(f" | Type: Digital | Download Size: {self.__download_size}MB | {self.get_fulfilment_info()}")

    def to_dict(self) -> dict:
        data = self._base_dict("digital")
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["download_size"])
