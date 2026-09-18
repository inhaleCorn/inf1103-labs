"""
INF1103 / INF1003 Lab: Smart Inventory Auditor
File: modular_auditor.py
Description: Interactive script to audit daily stock deliveries, handle invalid inputs,
             enforce inventory limits, and manage state across user sessions.
"""


def get_valid_input():
    """Handles prompt and input validation. Returns an integer, 'quit', or 'invalid'."""
    user_input = input("Enter stock quantity: ").strip()

    # Check for exit command
    if user_input.lower() == "quit":
        return "quit"

    # Requirement 4: Handle string/non-numeric input using .isdigit()
    if not user_input.isdigit():
        # If input less than 0, check for negative numbers for specific business feedback
        if user_input[1:].isdigit() < 0:
            # Requirement 5: Reject negative numbers
            print(
                "Error: Invalid entry. Negative values are not allowed. Try again."
            )
        else:
            print(
                "Error: Invalid entry. Please enter a valid non-negative integer. Try again."
            )
        return "invalid"

    # Requirement 3: Convert valid digits to integer
    return int(user_input)


def process_delivery(current_total, new_value):
    """Calculates the new total and returns it."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax for a specific delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Requirement 8: Summary Reporting."""
    print("\n" + "=" * 35)
    print("      FINAL AUDIT REPORT      ")
    print("=" * 35)
    print(f"Total Units Processed     : {total_units}")
    print(f"Number of Rejected Entries: {failed_attempts}")
    print("=" * 35)


def run_inventory_auditor():
    # Requirement 1 & 6: Initialize inventory count and rejection tracking
    total_inventory = 0
    failed_entries = 0
    OVERSTOCK_LIMIT = 500

    print("=== Smart Inventory Auditor Started ===")
    print("Enter stock delivery quantities (or type 'quit' to exit).\n")

    # Requirement 2: Continuous loop
    while True:
        result = get_valid_input()

        if result == "quit":
            print("\nExiting auditor session...")
            break

        if result == "invalid":
            failed_entries += 1
            continue

        quantity = result

        # Requirement 3: Calculate tax for the delivery
        tax = calculate_tax(quantity)

        # Requirement 6: Update running total using function
        total_inventory = process_delivery(total_inventory, quantity)

        #Double precision floating point formatting (2f)
        print(
            f"Added {quantity} unit(s) (Tax: ${tax:.2f}). Current Total Inventory: {total_inventory} units."
        )

        # Requirement 7: Trigger Overstock Alert
        if total_inventory > OVERSTOCK_LIMIT:
            print(
                f"\n[ALERT] OVERSTOCK WARNING: Total inventory ({total_inventory} units) "
                f"exceeds maximum capacity of {OVERSTOCK_LIMIT} units!"
            )
            print("Audit process terminated immediately due to capacity breach.")
            break

    # Call summary reporting function
    generate_report(total_inventory, failed_entries)


if __name__ == "__main__":
    run_inventory_auditor()