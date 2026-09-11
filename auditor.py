"""
INF1103 / INF1003 Lab: Smart Inventory Auditor
File: auditor.py
Description: Interactive script to audit daily stock deliveries, handle invalid inputs,
             enforce inventory limits, and manage state across user sessions.
"""


def run_inventory_auditor():
    # Requirement 1 & 6: Initialize inventory count and rejection tracking
    total_inventory = 0
    failed_entries = 0
    OVERSTOCK_LIMIT = 500

    print("=== Smart Inventory Auditor Started ===")
    print("Enter stock delivery quantities (or type 'quit' to exit).\n")

    # Requirement 2: Continuous loop
    while True:
        user_input = input("Enter stock quantity: ").strip()

        # Check for exit command
        if user_input.lower() == "quit":
            print("\nExiting auditor session...")
            break

        # Requirement 4: Handle string/non-numeric input using .isdigit()
        if not user_input.isdigit():
            # If input starts with '-' check for negative numbers for specific business feedback
            if user_input.startswith("-") and user_input[1:].isdigit():
                # Requirement 5: Reject negative numbers
                print(
                    "Error: Invalid entry. Negative values are not allowed. Try again."
                )
            else:
                print(
                    "Error: Invalid entry. Please enter a valid non-negative integer. Try again."
                )

            failed_entries += 1
            continue

        # Requirement 3: Convert valid digits to integer
        quantity = int(user_input)

        # Requirement 6: Update running total
        total_inventory += quantity
        print(
            f"Added {quantity} unit(s). Current Total Inventory: {total_inventory} units."
        )

        # Requirement 7: Trigger Overstock Alert
        if total_inventory > OVERSTOCK_LIMIT:
            print(
                f"\n[ALERT] OVERSTOCK WARNING: Total inventory ({total_inventory} units) "
                f"exceeds maximum capacity of {OVERSTOCK_LIMIT} units!"
            )
            print("Audit process terminated immediately due to capacity breach.")
            break

    # Requirement 8: Summary Reporting
    print("\n" + "=" * 35)
    print("      FINAL AUDIT REPORT      ")
    print("=" * 35)
    print(f"Total Units Processed     : {total_inventory}")
    print(f"Number of Rejected Entries: {failed_entries}")
    print("=" * 35)


if __name__ == "__main__":
    run_inventory_auditor()