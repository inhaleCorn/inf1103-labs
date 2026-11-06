"""
INF1103: Lab 8 - Object-Oriented Relationships Part 2
File: inventory_manager.py
Description: Main program (menu, input, persistence) for the Inventory Management System.
Relationships: Supplier-Product (association), Inventory-Product (aggregation),
Order-OrderLine (composition), plus Product inheritance from Lab 7.
"""

import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

INVENTORY_FILE = "inventory.json"
DEFAULT_SUPPLIER = Supplier("S000", "Unassigned Supplier", "n/a")


def create_product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    """Factory: builds the right subclass from the type tag, linking the shared Supplier object."""
    supplier = suppliers.get(data.get("supplier_id", DEFAULT_SUPPLIER.get_supplier_id()))
    if supplier is None:
        supplier = suppliers.setdefault(DEFAULT_SUPPLIER.get_supplier_id(), DEFAULT_SUPPLIER)
    if data.get("type") == "digital":
        return DigitalProduct.from_dict(data, supplier)
    return PhysicalProduct.from_dict(data, supplier)  # also covers old files with no type tag


def default_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    acme = Supplier("S001", "Acme Hardware", "sales@acme.example")
    softco = Supplier("S002", "SoftCo Digital", "support@softco.example")
    suppliers = {s.get_supplier_id(): s for s in (acme, softco)}
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, acme, 2.5))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, acme, 0.2))
    inventory.add_product(DigitalProduct("P003", "Antivirus Software", 49.99, 100, softco, 150.0))
    return inventory, suppliers


def load_inventory(filepath: str = INVENTORY_FILE) -> tuple[Inventory, dict[str, Supplier]]:
    """Loads suppliers and products. Accepts the older Lab 7 format (a plain list of products)."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            if isinstance(data, list):  # Lab 7 format
                data = {"suppliers": [], "products": data}
            suppliers = {d["id"]: Supplier.from_dict(d) for d in data.get("suppliers", [])}
            inventory = Inventory()
            for item in data.get("products", []):
                inventory.add_product(create_product_from_dict(item, suppliers))
            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return inventory, suppliers
        except Exception as e:
            print(f"[WARNING] Could not read '{filepath}' ({e}). Starting with default inventory.")
    print("inventory.json not found. Initializing with default inventory.")
    return default_inventory()


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier], filepath: str = INVENTORY_FILE) -> None:
    """Saves suppliers and products, preserving product types."""
    try:
        print("Saving inventory...")
        data = {
            "suppliers": [s.to_dict() for s in suppliers.values()],
            "products": [p.to_dict() for p in inventory.get_all_products()],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to {filepath}.")
    except Exception as e:
        print(f"[ERROR] Failed to save inventory data: {e}")


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    """Lets the user pick an existing Supplier or create a new one."""
    print("\nSuppliers:")
    for supplier in suppliers.values():
        supplier.display_information()
    choice = input("Enter Supplier ID, or N for a new supplier: ").strip()
    if choice.upper() == "N":
        name = input("Supplier Name: ").strip()
        email = input("Contact Email: ").strip()
        new_id = f"S{len(suppliers) + 1:03d}"
        while new_id in suppliers:
            new_id = f"S{int(new_id[1:]) + 1:03d}"
        supplier = Supplier(new_id, name, email)
        suppliers[new_id] = supplier
        print(f"Created supplier {new_id}.")
        return supplier
    supplier = suppliers.get(choice)
    if supplier is None:
        print("Error: Supplier not found.")
    return supplier


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    """Prompts for product type and details, then adds the product to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if inventory.find_product(product_id):
        print("Error: Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Error: Invalid input format for price or stock.")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Enter choice (1-2): ").strip()

    try:
        if choice == "1":
            weight = float(input("Weight (kg): "))
            if weight < 0:
                print("Error: Weight cannot be negative.")
                return
            new_product: Product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        elif choice == "2":
            download_size = float(input("Download Size (MB): "))
            if download_size < 0:
                print("Error: Download size cannot be negative.")
                return
            new_product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
        else:
            print("Error: Invalid product type selection.")
            return
    except ValueError:
        print("Error: Invalid numeric input.")
        return

    inventory.add_product(new_product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product:
        print("Product Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}")
        try:
            product.update_stock(int(input("New Stock Quantity: ")))
            print("Stock updated successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Product not found.")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product:
        print("Product Found")
        print("-" * 60)
        product.display_information()
        print("Supplier details:")
        product.get_supplier().display_information()
        print("-" * 60)
    else:
        print("Product not found.")


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip()
    removed = inventory.remove_product(product_id)
    if removed:
        print(f"Removed '{removed.get_name()}' from the inventory.")
    else:
        print("Product not found.")


def main() -> None:
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    inventory, suppliers = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Remove Product")
        print("7. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory, suppliers)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            save_inventory(inventory, suppliers)
        elif option == "6":
            remove_product(inventory)
        elif option == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
