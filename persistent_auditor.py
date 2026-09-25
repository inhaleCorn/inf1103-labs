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


