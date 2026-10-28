"""
INF1103: Lab 6 - Basics of Object-Oriented Programming
File: inventory_manager.py
Description: Refactored inventory management system using Product and Inventory classes.
"""

import json
import os

INVENTORY_FILE = "inventory.json"


class Product:
    """Represents and manages an individual product."""

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
        """Displays formatted product details matching the original output."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict:
        """Converts product instance data to dictionary for JSON persistence."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Product instance from dictionary data."""
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"]
        )


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
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

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
                    product = Product.from_dict(item)
                    inventory.add_product(product)
            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return inventory
        except Exception as e:
            print(f"[WARNING] Could not read '{filepath}' ({e}). Starting with default inventory.")

    print("inventory.json not found. Initializing with default inventory.")
    default_items = [
        Product("P001", "Laptop", 1200.00, 15),
        Product("P002", "Mouse", 25.50, 40),
        Product("P003", "Keyboard", 45.00, 25)
    ]
    for p in default_items:
        inventory.add_product(p)
    return inventory


def save_inventory(inventory: Inventory, filepath=INVENTORY_FILE):
    """Saves inventory data to inventory.json."""
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
    """Adds a new product object to the inventory."""
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

    new_product = Product(product_id, name, price, stock)
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
    """Searches for a product by ID and displays details using Product class methods."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product:
        print("Product Found")
        print("-" * 48)
        print(f"ID: {product.get_product_id()}")
        print(f"Name: {product.get_name()}")
        print(f"Price: ${product.get_price():.2f}")
        print(f"Stock: {product.get_stock()}")
        print("-" * 48)
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