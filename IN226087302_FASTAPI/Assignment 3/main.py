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

orders = [] # Will be populated via POST /orders during your tests

# --- Existing Endpoints (Search, Sort, Pagination) ---

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
    
    rev = (order == "desc")
    results = sorted(products, key=lambda p: p[sort_by], reverse=rev)
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

# --- New Assignment Endpoints (Q4, Q5, Q6) ---

@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    results = [o for o in orders if customer_name.lower() in o['customer_name'].lower()]
    if not results:
        return {"message": f"No orders found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(results), "orders": results}

@app.get("/products/sort-by-category")
def sort_by_category():
    # Sorts first by category (A-Z), then by price (Low-High)
    result = sorted(products, key=lambda p: (p['category'], p['price']))
    return {"products": result, "total": len(result)}

@app.get("/products/browse")
def browse_products(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query('price'),
    order: str = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):
    # 1. Search/Filter
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    # 2. Sort
    if sort_by in ['price', 'name']:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == 'desc'))

    # 3. Paginate
    total = len(result)
    start = (page - 1) * limit
    paged = result[start : start + limit]

    return {
        "keyword": keyword, "sort_by": sort_by, "order": order,
        "page": page, "limit": limit, "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }

# --- Bonus: Paginate Orders ---
@app.get("/orders/page")
def get_orders_paged(page: int = Query(1, ge=1), limit: int = Query(3, ge=1)):
    start = (page - 1) * limit
    return {
        "page": page,
        "limit": limit,
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start : start + limit]
    }

# --- POST endpoint to help you add data for testing ---
@app.post("/orders")
def place_order(customer_name: str, item_id: int):
    new_order = {"order_id": len(orders) + 1, "customer_name": customer_name, "item_id": item_id}
    orders.append(new_order)
    return new_order