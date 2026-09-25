"""
INF1103 / INF1003 Lab: Smart Inventory Auditor
File: persistent_auditor.py
Description: Interactive script to audit daily stock deliveries, handle invalid inputs,
             enforce inventory limits, and manage state across user sessions using persistent storage.
"""

import os

INVENTORY_FILE = "inventory.txt"


def load_inventory(filepath=INVENTORY_FILE):
    """
    Requirement 1 & 4: Reads total inventory and history from file if it exists.
    If file doesn't exist, starts with 0 and an empty list without throwing an error.
    """
    if not os.path.exists(filepath):
        print(f"[INFO] '{filepath}' not found. Starting with clean inventory.\n")
        return 0, []

    try:
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            return 0, []

        total_inventory = int(lines[0])
        history = []
        if len(lines) > 1 and lines[1]:
            history = [int(x) for x in lines[1].split(",") if x.strip().isdigit()]

        print(f"[INFO] Loaded existing state: Total = {total_inventory}, History = {history}\n")
        return total_inventory, history
    except Exception as e:
        print(f"[WARNING] Could not read '{filepath}' ({e}). Starting fresh.\n")
        return 0, []

def save_inventory(total_inventory, history, filepath=INVENTORY_FILE):
    """
    Requirement 3 & 4: Saves final total and transaction history list to disk.
    Line 1: Total inventory integer
    Line 2: Comma-separated history list
    """
    try:
        with open(filepath, "w") as f:
            f.write(f"{total_inventory}\n")
            f.write(",".join(map(str, history)) + "\n")
        print(f"\n[INFO] Data saved successfully to '{filepath}'.")
    except Exception as e:
        print(f"\n[ERROR] Failed to save inventory data: {e}")

def get_valid_input():
    """Handles prompt and input validation. Returns an integer, 'quit', or 'invalid'."""
    user_input = input("Enter stock quantity: ").strip()

    if user_input.lower() == "quit":
        return "quit"

    # Check for negative numbers correctly
    if user_input.startswith("-") and user_input[1:].isdigit():
        print("Error: Invalid entry. Negative values are not allowed. Try again.")
        return "invalid"

    # Check for string/non-numeric input
    if not user_input.isdigit():
        print("Error: Invalid entry. Please enter a valid non-negative integer. Try again.")
        return "invalid"

    return int(user_input)


def process_delivery(current_total, new_value):
    """Calculates the new total and returns it."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax for a specific delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, history):
    """Requirement 8: Summary Reporting with history display."""
    print("\n" + "=" * 40)
    print("           FINAL AUDIT REPORT           ")
    print("=" * 40)
    print(f"Total Units Processed     : {total_units}")
    print(f"Number of Rejected Entries: {failed_attempts}")
    print(f"Transaction History       : {history}")
    print("=" * 40)


def run_inventory_auditor():
    # Requirement 1: Load previous state or initialize clean session
    total_inventory, transaction_history = load_inventory()
    failed_entries = 0
    OVERSTOCK_LIMIT = 500

    print("=== Smart Inventory Auditor Started ===")
    print("Enter stock delivery quantities (or type 'quit' to exit).\n")

    while True:
        result = get_valid_input()

        if result == "quit":
            print("\nExiting auditor session...")
            break

        if result == "invalid":
            failed_entries += 1
            continue

        quantity = result

        # Requirement 2: Store transaction amount in history list
        transaction_history.append(quantity)

        tax = calculate_tax(quantity)
        total_inventory = process_delivery(total_inventory, quantity)

        print(
            f"Added {quantity} unit(s) (Tax: ${tax:.2f}). Current Total Inventory: {total_inventory} units."
        )

        if total_inventory > OVERSTOCK_LIMIT:
            print(
                f"\n[ALERT] OVERSTOCK WARNING: Total inventory ({total_inventory} units) "
                f"exceeds maximum capacity of {OVERSTOCK_LIMIT} units!"
            )
            print("Audit process terminated immediately due to capacity breach.")
            break

    # Requirement 3: Save data back to disk on session exit
    save_inventory(total_inventory, transaction_history)

    generate_report(total_inventory, failed_entries, transaction_history)


if name == "__main__":
    run_inventory_auditor()
