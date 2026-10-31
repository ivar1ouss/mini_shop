from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)

app.secret_key = 'super_secret_key_for_shop'

PRODUCTS = [
    {"id": 1, "name": "Смартфон", "price": 25000, "category": "Электроника"},
    {"id": 2, "name": "Ноутбук", "price": 65000, "category": "Электроника"},
    {"id": 3, "name": "Наушники", "price": 3500, "category": "Аксессуары"},
    {"id": 4, "name": "Книга по C#", "price": 1500, "category": "Книги"},
    {"id": 5, "name": "Кофеварка", "price": 8000, "category": "Бытовая техника"},
]


@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)


@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return "Товар не найден", 404
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    str_id = str(product_id)

    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1

    session['cart'] = cart
    flash(f"Товар '{product['name']}' добавлен в корзину!", "success")

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_data = session.get('cart', {})
    cart_items = []
    total_sum = 0

    for product_id, qty in cart_data.items():
        product = next((p for p in PRODUCTS if p["id"] == int(product_id)), None)
        if product:
            item_total = product['price'] * qty
            total_sum += item_total
            cart_items.append({
                "product": product,
                "qty": qty,
                "item_total": item_total
            })

    return render_template('cart.html', cart_items=cart_items, total_sum=total_sum)


@app.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    str_id = str(product_id)

    if str_id in cart:
        del cart[str_id]
        session['cart'] = cart
        flash("Товар удален из корзины", "success")

    return redirect(url_for('cart'))


@app.route('/clear')
def clear_cart():
    session.pop('cart', None)
    flash("Корзина полностью очищена", "success")
    return redirect(url_for('cart'))


@app.route('/stats')
def stats():
    cart_data = session.get('cart', {})
    total_items = sum(cart_data.values())
    unique_items = len(cart_data)

    total_sum = 0
    for product_id, qty in cart_data.items():
        product = next((p for p in PRODUCTS if p["id"] == int(product_id)), None)
        if product:
            total_sum += product['price'] * qty
    return render_template('stats.html', total_items=total_items, unique_items=unique_items, total_sum=total_sum)


if __name__ == '__main__':
    app.run(debug=True)