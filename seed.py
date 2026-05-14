"""Run once to seed the database with sample data matching your original DDL."""
from app import app
from database import db, Customer, Seller, Product, Order, OrderItem
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    # Sellers
    sellers = [
        Seller(seller_name='SellerA', join_date=date(2023,1,1), source='import'),
        Seller(seller_name='SellerB', join_date=date(2023,2,1), source='import'),
        Seller(seller_name='SellerC', join_date=date(2023,3,1), source='manual'),
        Seller(seller_name='SellerD', join_date=date(2023,4,1), source='manual'),
        Seller(seller_name='SellerE', join_date=date(2023,5,1), source='import'),
    ]
    db.session.add_all(sellers)
    db.session.flush()

    # Customers
    customers = [
        Customer(name='Priya', email='priya@gmail.com', created_at=date(2024,1,1), created_by='admin'),
        Customer(name='Padma', email='padma@gmail.com', created_at=date(2024,2,1), created_by='admin'),
        Customer(name='Ram',   email='ram@gmail.com',   created_at=date(2024,3,1), created_by='system'),
        Customer(name='David', email='david@gmail.com', created_at=date(2024,4,1), created_by='system'),
        Customer(name='Elena', email='elena@gmail.com', created_at=date(2024,5,1), created_by='admin'),
    ]
    db.session.add_all(customers)
    db.session.flush()

    # Products
    products = [
        Product(product_name='Laptop',     price=1000, seller_id=sellers[0].seller_id, note='high-end'),
        Product(product_name='Phone',      price=500,  seller_id=sellers[1].seller_id, note='mid-range'),
        Product(product_name='Tablet',     price=300,  seller_id=sellers[2].seller_id, note='budget'),
        Product(product_name='Headphones', price=100,  seller_id=sellers[3].seller_id, note='accessory'),
        Product(product_name='Monitor',    price=200,  seller_id=sellers[4].seller_id, note='display'),
    ]
    db.session.add_all(products)
    db.session.flush()

    # Orders
    orders = [
        Order(customer_id=customers[0].customer_id, order_date=date(2024,6,1), status='shipped'),
        Order(customer_id=customers[1].customer_id, order_date=date(2024,6,2), status='pending'),
        Order(customer_id=customers[2].customer_id, order_date=date(2024,6,3), status='delivered'),
        Order(customer_id=customers[3].customer_id, order_date=date(2024,6,4), status='cancelled'),
        Order(customer_id=customers[4].customer_id, order_date=date(2024,6,5), status='shipped'),
    ]
    db.session.add_all(orders)
    db.session.flush()

    # Order Items
    items = [
        OrderItem(order_id=orders[0].order_id, product_id=products[0].product_id, quantity=2, total_price=2000, flag='ok'),
        OrderItem(order_id=orders[1].order_id, product_id=products[1].product_id, quantity=1, total_price=500,  flag='ok'),
        OrderItem(order_id=orders[2].order_id, product_id=products[2].product_id, quantity=3, total_price=900,  flag='ok'),
        OrderItem(order_id=orders[3].order_id, product_id=products[3].product_id, quantity=1, total_price=100,  flag='ok'),
        OrderItem(order_id=orders[4].order_id, product_id=products[4].product_id, quantity=2, total_price=400,  flag='ok'),
    ]
    db.session.add_all(items)
    db.session.commit()

    print("✅ Database seeded successfully!")
