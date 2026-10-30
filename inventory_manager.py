"""
INF1103: Lab 7 - Object-Oriented Relationships Part 1 (Inheritance, Overriding, Abstract, Interfaces)
File: inventory_manager.py
Description: Refactored inventory management system with Inheritance, Abstract Classes, and Interfaces.
"""

from abc import ABC, abstractmethod
import json
import os

INVENTORY_FILE = "inventory.json"


class CanBeShipped(ABC):
    """Interface-style abstract base class for items that require shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns the shipping cost for the product."""
        pass


class Product(ABC):
    """Abstract base class representing an individual product."""

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, new_stock: int) -> None:
        """Updates the stock quantity of the product."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = new_stock

    def display_information(self) -> None:
        """Displays base product details."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method to return product fulfilment details."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Abstract method to convert product instance to dictionary for JSON persistence."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Abstract class method to create a Product instance from dictionary data."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product that requires shipping and has weight."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "Fulfilment: Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on weight ($5.00 base + $2.00 per kg)."""
        return 5.00 + (2.00 * self.__weight)

    def display_information(self) -> None:
        """Overrides display_information to include weight, shipping cost, and fulfilment info."""
        super().display_information()
        print(f" | Type: Physical | Weight: {self.__weight}kg | Shipping: ${self.calculate_shipping_cost():.2f} | {self.get_fulfilment_info()}")

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "weight": self.__weight
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            weight=data["weight"]
        )


class DigitalProduct(Product):
    """Represents a digital product delivered online with a download size."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Fulfilment: Delivered digitally via download link."

    def display_information(self) -> None:
        """Overrides display_information to include download size and fulfilment info."""
        super().display_information()
        print(f" | Type: Digital | Download Size: {self.__download_size}MB | {self.get_fulfilment_info()}")

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "download_size": self.__download_size
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            download_size=data["download_size"]
        )


def create_product_from_dict(data: dict) -> Product:
    """Factory function to instantiate the correct product subclass based on the type identifier."""
    prod_type = data.get("type")
    if prod_type == "digital":
        return DigitalProduct.from_dict(data)
    else:
        # Defaults to physical for backwards compatibility or missing type tags
        return PhysicalProduct.from_dict(data)


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product: Product) -> bool:
        """Adds a product to the inventory if the ID does not already exist."""
        if self.search_product(product.get_product_id()):
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id: str) -> Product:
        """Searches for a product by its Product ID."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        """Displays all products in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 80)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 80)

    def get_all_products(self) -> list:
        """Returns the list of Product instances."""
        return self.__products


def load_inventory(filepath=INVENTORY_FILE) -> Inventory:
    """
    Checks whether inventory.json exists. Loads inventory if it exists.
    Otherwise, initializes with default inventory products.
    """
    inventory = Inventory()

    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    product = create_product_from_dict(item)
                    inventory.add_product(product)
            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return inventory
        except Exception as e:
            print(f"[WARNING] Could not read '{filepath}' ({e}). Starting with default inventory.")

    print("inventory.json not found. Initializing with default inventory.")
    default_items = [
        PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5),
        PhysicalProduct("P002", "Mouse", 25.50, 40, 0.2),
        DigitalProduct("P003", "Antivirus Software", 49.99, 100, 150.0)
    ]
    for p in default_items:
        inventory.add_product(p)
    return inventory


def save_inventory(inventory: Inventory, filepath=INVENTORY_FILE):
    """Saves inventory data to inventory.json preserving product types."""
    try:
        print("Saving inventory...")
        data = [product.to_dict() for product in inventory.get_all_products()]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to {filepath}.")
    except Exception as e:
        print(f"[ERROR] Failed to save inventory data: {e}")


def display_all(inventory: Inventory):
    """Delegates displaying all products to the Inventory object."""
    inventory.display_all()


def add_product(inventory: Inventory):
    """Prompts user for product type and details, then adds to inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id):
        print("Error: Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Error: Invalid input format for price or stock.")
        return

    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Enter choice (1-2): ").strip()

    if choice == "1":
        try:
            weight = float(input("Weight (kg): "))
            if weight < 0:
                print("Error: Weight cannot be negative.")
                return
            new_product = PhysicalProduct(product_id, name, price, stock, weight)
        except ValueError:
            print("Error: Invalid input format for weight.")
            return
    elif choice == "2":
        try:
            download_size = float(input("Download Size (MB): "))
            if download_size < 0:
                print("Error: Download size cannot be negative.")
                return
            new_product = DigitalProduct(product_id, name, price, stock, download_size)
        except ValueError:
            print("Error: Invalid input format for download size.")
            return
    else:
        print("Error: Invalid product type selection.")
        return

    inventory.add_product(new_product)
    print("Product added successfully!")


def update_stock(inventory: Inventory):
    """Updates the stock quantity of an existing product using Product methods."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product:
        print("Product Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}")
        try:
            new_stock = int(input("New Stock Quantity: "))
            product.update_stock(new_stock)
            print("Stock updated successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Product not found.")


def search_product(inventory: Inventory):
    """Searches for a product by ID and displays polymorphically formatted details."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product:
        print("Product Found")
        print("-" * 60)
        product.display_information()
        print("-" * 60)
    else:
        print("Product not found.")


def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()