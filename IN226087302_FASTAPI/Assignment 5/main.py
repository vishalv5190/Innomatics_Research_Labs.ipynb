from fastapi import FastAPI, Query, status
from typing import Optional

app = FastAPI()

# --- Initial Data ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = [] # Populated via POST /orders

# --- Q1-Q3: Search, Sort, Page (Existing Endpoints) ---

@app.get("/products/search")
def search_products(keyword: str):
    results = [p for p in products if keyword.lower() in p['name'].lower()]
    if not results:
        return {"message": f"No products found for: {keyword}"}
    return {"keyword": keyword, "total_found": len(results), "products": results}

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}
    results = sorted(products, key=lambda p: p[sort_by], reverse=(order == 'desc'))
    return {"sort_by": sort_by, "order": order, "products": results}

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    paged_data = products[start : start + limit]
    return {
        "page": page,
        "limit": limit,
        "total_pages": -(-len(products) // limit),
        "products": paged_data
    }

# --- Q4: Search Orders ---
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    results = [o for o in orders if customer_name.lower() in o['customer_name'].lower()]
    if not results:
        return {"message": f"No orders found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(results), "orders": results}

# --- Q5: Advanced Category Sort ---
@app.get("/products/sort-by-category")
def sort_by_category():
    # Sorts by category (A-Z) then price (Ascending)
    result = sorted(products, key=lambda p: (p['category'], p['price']))
    return {"products": result, "total": len(result)}

# --- Q6: The "Smart" Browse Endpoint ---
@app.get("/products/browse")
def browse_products(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query('price'),
    order: str = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):
    # Step 1: Search
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    # Step 2: Sort
    if sort_by in ['price', 'name']:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == 'desc'))

    # Step 3: Paginate
    total = len(result)
    start = (page - 1) * limit
    paged = result[start : start + limit]

    return {
        "keyword": keyword, "sort_by": sort_by, "order": order,
        "page": page, "limit": limit, "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }

# --- Helper for Testing (POST Orders) ---
@app.post("/orders")
def create_order(customer_name: str, product_id: int):
    new_order = {"order_id": len(orders) + 1, "customer_name": customer_name, "product_id": product_id}
    orders.append(new_order)
    return new_order