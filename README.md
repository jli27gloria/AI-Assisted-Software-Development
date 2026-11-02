# Inventory CLI

A Python command-line tool for managing a product inventory, stored in a local JSON file.

## Requirements
Python 3.9+ (no external packages)

## Usage
```bash
python3 inventory.py add --item_name "Water" --description "500ml bottle" --price 1.99 --in_stock 50
python3 inventory.py list
python3 inventory.py get 1
python3 inventory.py update 1 --price 2.49
python3 inventory.py delete 1
```

Data is saved to `products.json` (created automatically on first run).