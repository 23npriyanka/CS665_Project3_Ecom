from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Customer, Seller, Product, Order, OrderItem
from sqlalchemy import func, text
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key-here'

db.init_app(app)

# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    total_customers = db.session.query(func.count(Customer.customer_id)).scalar()
    total_sellers   = db.session.query(func.count(Seller.seller_id)).scalar()
    total_products  = db.session.query(func.count(Product.product_id)).scalar()
    total_orders    = db.session.query(func.count(Order.order_id)).scalar()
    total_revenue   = db.session.query(func.sum(OrderItem.total_price)).scalar() or 0
    avg_order_value = db.session.query(func.avg(OrderItem.total_price)).scalar() or 0

    top_customers = (
        db.session.query(Customer.name, func.count(Order.order_id).label('order_count'))
        .join(Order, Customer.customer_id == Order.customer_id)
        .group_by(Customer.customer_id)
        .order_by(func.count(Order.order_id).desc())
        .limit(5).all()
    )

    orders_by_status = (
        db.session.query(Order.status, func.count(Order.order_id).label('cnt'))
        .group_by(Order.status).all()
    )

    return render_template('dashboard.html',
        total_customers=total_customers,
        total_sellers=total_sellers,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        avg_order_value=round(avg_order_value, 2),
        top_customers=top_customers,
        orders_by_status=orders_by_status,
    )

# ─── CUSTOMERS ────────────────────────────────────────────────────────────────

@app.route('/customers')
def customers():
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not email:
            flash('Name and email are required.', 'danger')
            return redirect(url_for('add_customer'))
        if '@' not in email:
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('add_customer'))
        if Customer.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('add_customer'))
        c = Customer(name=name, email=email, created_at=date.today(), created_by='admin')
        db.session.add(c)
        db.session.commit()
        flash(f'Customer "{name}" added successfully!', 'success')
        return redirect(url_for('customers'))
    return render_template('customer_form.html', action='Add', customer=None)

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    c = Customer.query.get_or_404(id)
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not email:
            flash('Name and email are required.', 'danger')
            return redirect(url_for('edit_customer', id=id))
        if '@' not in email:
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('edit_customer', id=id))
        existing = Customer.query.filter_by(email=email).first()
        if existing and existing.customer_id != id:
            flash('Email already in use by another customer.', 'danger')
            return redirect(url_for('edit_customer', id=id))
        c.name = name
        c.email = email
        db.session.commit()
        flash('Customer updated.', 'success')
        return redirect(url_for('customers'))
    return render_template('customer_form.html', action='Edit', customer=c)

@app.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    c = Customer.query.get_or_404(id)
    if c.orders:
        flash('Cannot delete customer with existing orders.', 'danger')
        return redirect(url_for('customers'))
    db.session.delete(c)
    db.session.commit()
    flash('Customer deleted.', 'success')
    return redirect(url_for('customers'))

@app.route('/customers/<int:id>/orders')
def customer_orders(id):
    c = Customer.query.get_or_404(id)
    return render_template('customer_orders.html', customer=c)

# ─── PRODUCTS ─────────────────────────────────────────────────────────────────

@app.route('/products')
def products():
    all_products = Product.query.join(Seller).all()
    return render_template('products.html', products=all_products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    sellers = Seller.query.all()
    if request.method == 'POST':
        name      = request.form.get('product_name', '').strip()
        price_str = request.form.get('price', '').strip()
        seller_id = request.form.get('seller_id')
        note      = request.form.get('note', '').strip()
        if not name or not price_str or not seller_id:
            flash('All fields are required.', 'danger')
            return render_template('product_form.html', action='Add', product=None, sellers=sellers)
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Price must be a non-negative number.', 'danger')
            return render_template('product_form.html', action='Add', product=None, sellers=sellers)
        p = Product(product_name=name, price=price, seller_id=int(seller_id), note=note)
        db.session.add(p)
        db.session.commit()
        flash(f'Product "{name}" added.', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', action='Add', product=None, sellers=sellers)

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    p = Product.query.get_or_404(id)
    sellers = Seller.query.all()
    if request.method == 'POST':
        name      = request.form.get('product_name', '').strip()
        price_str = request.form.get('price', '').strip()
        seller_id = request.form.get('seller_id')
        note      = request.form.get('note', '').strip()
        if not name or not price_str or not seller_id:
            flash('All fields are required.', 'danger')
            return render_template('product_form.html', action='Edit', product=p, sellers=sellers)
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Price must be a non-negative number.', 'danger')
            return render_template('product_form.html', action='Edit', product=p, sellers=sellers)
        p.product_name = name
        p.price        = price
        p.seller_id    = int(seller_id)
        p.note         = note
        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', action='Edit', product=p, sellers=sellers)

@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    p = Product.query.get_or_404(id)
    if p.order_items:
        flash('Cannot delete product that appears in existing orders.', 'danger')
        return redirect(url_for('products'))
    db.session.delete(p)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('products'))

# ─── ORDERS ───────────────────────────────────────────────────────────────────

@app.route('/orders')
def orders():
    all_orders = Order.query.join(Customer).all()
    return render_template('orders.html', orders=all_orders)

@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    customers = Customer.query.all()
    products  = Product.query.all()
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        product_ids = request.form.getlist('product_id[]')
        quantities  = request.form.getlist('quantity[]')
        if not customer_id or not product_ids:
            flash('Please select a customer and at least one product.', 'danger')
            return render_template('order_form.html', customers=customers, products=products)
        # Validate quantities
        qty_list = []
        for q in quantities:
            try:
                val = int(q)
                if val < 1:
                    raise ValueError
                qty_list.append(val)
            except ValueError:
                flash('Quantities must be positive integers.', 'danger')
                return render_template('order_form.html', customers=customers, products=products)
        # TRANSACTION: create order + order items atomically
        try:
            order = Order(customer_id=int(customer_id), order_date=date.today(), status='pending')
            db.session.add(order)
            db.session.flush()   # get order.order_id before commit

            for pid, qty in zip(product_ids, qty_list):
                product = Product.query.get(int(pid))
                if not product:
                    raise ValueError(f'Product {pid} not found')
                item = OrderItem(
                    order_id=order.order_id,
                    product_id=int(pid),
                    quantity=qty,
                    total_price=round(product.price * qty, 2),
                    flag='ok'
                )
                db.session.add(item)
            db.session.commit()
            flash(f'Order #{order.order_id} created successfully!', 'success')
            return redirect(url_for('orders'))
        except Exception as e:
            db.session.rollback()
            flash(f'Transaction failed: {str(e)}', 'danger')
    return render_template('order_form.html', customers=customers, products=products)

@app.route('/orders/edit/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    o = Order.query.get_or_404(id)
    if request.method == 'POST':
        status = request.form.get('status', '').strip()
        valid_statuses = ['pending', 'shipped', 'delivered', 'cancelled']
        if status.lower() not in valid_statuses:
            flash('Invalid status value.', 'danger')
            return render_template('order_edit.html', order=o)
        o.status = status.lower()
        db.session.commit()
        flash('Order status updated.', 'success')
        return redirect(url_for('orders'))
    return render_template('order_edit.html', order=o)

@app.route('/orders/delete/<int:id>', methods=['POST'])
def delete_order(id):
    o = Order.query.get_or_404(id)
    try:
        for item in o.items:
            db.session.delete(item)
        db.session.delete(o)
        db.session.commit()
        flash('Order deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Could not delete order: {str(e)}', 'danger')
    return redirect(url_for('orders'))

# ─── SELLERS ──────────────────────────────────────────────────────────────────

@app.route('/sellers')
def sellers():
    all_sellers = Seller.query.all()
    return render_template('sellers.html', sellers=all_sellers)

@app.route('/sellers/add', methods=['GET', 'POST'])
def add_seller():
    if request.method == 'POST':
        name   = request.form.get('seller_name', '').strip()
        source = request.form.get('source', '').strip()
        if not name:
            flash('Seller name is required.', 'danger')
            return redirect(url_for('add_seller'))
        s = Seller(seller_name=name, join_date=date.today(), source=source)
        db.session.add(s)
        db.session.commit()
        flash(f'Seller "{name}" added.', 'success')
        return redirect(url_for('sellers'))
    return render_template('seller_form.html', action='Add', seller=None)

@app.route('/sellers/edit/<int:id>', methods=['GET', 'POST'])
def edit_seller(id):
    s = Seller.query.get_or_404(id)
    if request.method == 'POST':
        name   = request.form.get('seller_name', '').strip()
        source = request.form.get('source', '').strip()
        if not name:
            flash('Seller name is required.', 'danger')
            return redirect(url_for('edit_seller', id=id))
        s.seller_name = name
        s.source      = source
        db.session.commit()
        flash('Seller updated.', 'success')
        return redirect(url_for('sellers'))
    return render_template('seller_form.html', action='Edit', seller=s)

@app.route('/sellers/delete/<int:id>', methods=['POST'])
def delete_seller(id):
    s = Seller.query.get_or_404(id)
    if s.products:
        flash('Cannot delete seller with existing products.', 'danger')
        return redirect(url_for('sellers'))
    db.session.delete(s)
    db.session.commit()
    flash('Seller deleted.', 'success')
    return redirect(url_for('sellers'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
