from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    created_at  = db.Column(db.Date, nullable=False)
    created_by  = db.Column(db.String(50))
    orders      = db.relationship('Order', back_populates='customer', lazy=True)

class Seller(db.Model):
    __tablename__ = 'sellers'
    seller_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_name = db.Column(db.String(100), nullable=False)
    join_date   = db.Column(db.Date, nullable=False)
    source      = db.Column(db.String(50))
    products    = db.relationship('Product', back_populates='seller', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    product_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    price        = db.Column(db.Numeric(10, 2), nullable=False)
    seller_id    = db.Column(db.Integer, db.ForeignKey('sellers.seller_id'), nullable=False)
    note         = db.Column(db.String(100))
    seller       = db.relationship('Seller', back_populates='products')
    order_items  = db.relationship('OrderItem', back_populates='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    order_date  = db.Column(db.Date, nullable=False)
    status      = db.Column(db.String(50), default='pending')
    customer    = db.relationship('Customer', back_populates='orders')
    items       = db.relationship('OrderItem', back_populates='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id      = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id    = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity      = db.Column(db.Integer, nullable=False)
    total_price   = db.Column(db.Numeric(10, 2))
    flag          = db.Column(db.String(50), default='ok')
    order         = db.relationship('Order', back_populates='items')
    product       = db.relationship('Product', back_populates='order_items')
