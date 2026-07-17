import json
import os

DATA_FILE = "bank_data.json"


def load_data():
    """Load account data from the JSON file (acts as a simple database)."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data):
    """Persist account data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
