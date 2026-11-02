import argparse 
import json
import os
from datetime import date

DATA_FILE = "products.json"

def load_products():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_products(products):
    with open(DATA_FILE, "w") as f:
        json.dump(products, f, indent=2)


# add a new product to the inventory

def add_product(item_name, description, price, in_stock):
    products = load_products()

    if products:
        new_id = max(p["id"] for p in products) + 1
    else:
        new_id = 1

    product = {
        "id": new_id,
        "item_name": item_name,
        "description": description,
        "price": price,
        "in_stock": in_stock,
        "date": date.today().isoformat(),
    }

    products.append(product)
    save_products(products)
    print(f"Added product #{new_id}: {item_name}")





def find_product(products, product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


def list_products():
    products = load_products()
    if not products:
        print("No products found.")
        return
    for p in products:
        print(f'#{p["id"]} {p["item_name"]} | ${p["price"]:.2f} | stock: {p["in_stock"]} | {p["date"]}')


def get_product(product_id):
    products = load_products()
    p = find_product(products, product_id)
    if p is None:
        print(f"Product #{product_id} not found.")
        return
    print(json.dumps(p, indent=2))


def delete_product(product_id):
    products = load_products()
    p = find_product(products, product_id)
    if p is None:
        print(f"Product #{product_id} not found.")
        return
    products.remove(p)
    save_products(products)
    print(f"Deleted product #{product_id}.")


def update_product(product_id, item_name=None, description=None, price=None, in_stock=None):
    products = load_products()
    p = find_product(products, product_id)
    if p is None:
        print(f"Product #{product_id} not found.")
        return

    if item_name is not None:
        p["item_name"] = item_name
    if description is not None:
        p["description"] = description
    if price is not None:
        p["price"] = price
    if in_stock is not None:
        p["in_stock"] = in_stock

    save_products(products)
    print(f"Updated product #{product_id}.")

def main():
    parser = argparse.ArgumentParser(description="Product inventory CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new product")
    p_add.add_argument("--item_name", required=True)
    p_add.add_argument("--description", default="")
    p_add.add_argument("--price", type=float, required=True)
    p_add.add_argument("--in_stock", type=int, required=True)

    # list
    sub.add_parser("list", help="List all products")

    # get
    p_get = sub.add_parser("get", help="Show one product")
    p_get.add_argument("id", type=int)

    # update
    p_up = sub.add_parser("update", help="Update a product")
    p_up.add_argument("id", type=int)
    p_up.add_argument("--item_name")
    p_up.add_argument("--description")
    p_up.add_argument("--price", type=float)
    p_up.add_argument("--in_stock", type=int)

    # delete
    p_del = sub.add_parser("delete", help="Delete a product")
    p_del.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_product(args.item_name, args.description, args.price, args.in_stock)
    elif args.command == "list":
        list_products()
    elif args.command == "get":
        get_product(args.id)
    elif args.command == "update":
        update_product(args.id, args.item_name, args.description, args.price, args.in_stock)
    elif args.command == "delete":
        delete_product(args.id)


if __name__ == "__main__":
    main()