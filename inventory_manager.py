"""
INF1103: Lab 5 - Data Manipulation
File: inventory_manager.py
Description: Inventory management system using dictionaries, lists, and JSON persistence.
"""

import json
import os

INVENTORY_FILE = "inventory.json"


def load_inventory(filepath=INVENTORY_FILE):
    """
    Checks whether inventory.json exists. Loads inventory if it exists.
    Otherwise, initializes with default inventory products.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                inventory = json.load(f)
            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return inventory
        except Exception as e:
            print(f"[WARNING] Could not read '{filepath}' ({e}). Starting with default inventory.")
    
    print("inventory.json not found. Initializing with default inventory.")
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
    ]


def save_inventory(inventory, filepath=INVENTORY_FILE):
    """Saves inventory data to inventory.json."""
    try:
        print("Saving inventory...")
        with open(filepath, "w") as f:
            json.dump(inventory, f, indent=4)
        print(f"Inventory saved successfully to {filepath}.")
    except Exception as e:
        print(f"[ERROR] Failed to save inventory data: {e}")


def display_all(inventory):
    """Displays all products in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    else:
        for item in inventory:
            print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 48)


def add_product(inventory):
    """Adds a new product to the inventory list."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    for item in inventory:
        if item['id'] == product_id:
            print("Error: Product ID already exists!")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Error: Invalid input format for price or stock.")
        return

    new_item = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_item)
    print("Product added successfully!")


def update_stock(inventory):
    """Updates the stock quantity of an existing product by ID."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    
    found = False
    for item in inventory:
        if item['id'] == product_id:
            found = True
            print("Product Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}")
            try:
                new_stock = int(input("New Stock Quantity: "))
                item['stock'] = new_stock
                print("Stock updated successfully!")
            except ValueError:
                print("Error: Invalid stock quantity entered.")
            break
            
    if not found:
        print("Product not found.")


def search_product(inventory):
    """Searches for a product by its ID and displays its details."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    
    found = False
    for item in inventory:
        if item['id'] == product_id:
            found = True
            print("Product Found")
            print("-" * 48)
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("-" * 48)
            break
            
    if not found:
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