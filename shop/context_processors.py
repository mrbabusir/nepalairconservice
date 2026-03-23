from decimal import Decimal

def cart_totals(request):
    cart = request.session.get("cart", {})
    total_items = sum(item["qty"] for item in cart.values())
    total_price = sum(
        Decimal(str(item["price"])) * item["qty"]
        for item in cart.values()
    )
    return {
        "cart_total_items": total_items,
        "cart_total_price": round(float(total_price), 2),
    }