from storeapp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint, ForeignKeyConstraint
from flask_login import UserMixin
import jwt
from time import time
from flask import current_app 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='buyer')
    image_file = db.Column(db.String(50), nullable=False,
                           default='default.jpg')
    address = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    town = db.Column(db.String(50), nullable=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    products = db.relationship('Product', backref='user', lazy=True)

    def get_confirm_token(self, expires_sec=10000):
        return jwt.encode({'confirm_user': self.email,
                            'exp': time() + expires_sec}, 
                            key=current_app.config['SECRET_KEY'])
    
    @staticmethod
    def verify_confirm_token(token):
        try:
            email = jwt.decode(token, algorithms=[
                                  'HS256'], key=current_app.config['SECRET_KEY'])['confirm_user']
            print("email isss------------",email)
        except:
            return None
        return User.query.filter_by(email=email).first()
    
    def get_reset_token(self, expires_sec=10000):
        return jwt.encode({'reset_password': self.username,
                            'exp': time() + expires_sec}, 
                            key=current_app.config['SECRET_KEY'])
    
    @staticmethod
    def verify_reset_token(token):
        try:
            username = jwt.decode(token, algorithms=[
                                  'HS256'], key=current_app.config['SECRET_KEY'])['reset_password']
            print("email isss------------",username)
        except:
            return None
        return User.query.filter_by(username=username).first()
    
    
    def is_admin(self):
        return self.role == 'admin'

    def is_seller(self):
        return self.role == 'seller'

    def is_buyer(self):
        return self.role == 'buyer'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)


# Association table to link properties to products
product_properties = db.Table('product_properties',
                              db.Column('product_id', db.Integer, db.ForeignKey(
                                  'product.id'), primary_key=True),
                              db.Column('property_id', db.Integer, db.ForeignKey(
                                  'property.id'), primary_key=True)
                              )

# Association table to link properties to variations
variation_properties = db.Table('variation_properties',
                                db.Column('variation_id', db.Integer, db.ForeignKey(
                                    'variation.id'), primary_key=True),
                                db.Column('property_id', db.Integer, db.ForeignKey(
                                    'property.id'), primary_key=True)
                                )


class Variation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False) #ADD QUANTITY,IMAGE3
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    properties = db.relationship('Property', secondary=variation_properties, lazy='subquery',
                                 backref=db.backref('variations', lazy=True))

    def __repr__(self):
        return f'<Variation {self.name}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)  #ADD QUANTITY,IMAGE3
    variations = db.relationship('Variation', backref='product', lazy=True)
    properties = db.relationship('Property', secondary=product_properties, lazy='subquery',
                                 backref=db.backref('products', lazy=True))
    product_type = db.Column(
        db.String(20), nullable=False, server_default='physical')
    __table_args__ = (
        CheckConstraint(product_type.in_(
            ('physical', 'digital')), name='valid_product_type'),
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    variation_id = db.Column(db.Integer, db.ForeignKey(
        'variation.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    shipping_address = db.Column(db.String(200))
    billing_address = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False, server_default='pending')
    __table_args__ = (
        CheckConstraint(status.in_(('pending', 'processing',
                        'completed', 'cancelled')), name='valid_order_status'),
        ForeignKeyConstraint(['user_id'], ['user.id']),
        ForeignKeyConstraint(['product_id'], ['product.id']),
        ForeignKeyConstraint(['variation_id'], ['variation.id'])
    )
    processed_on = db.Column(db.DateTime, nullable=True)
    cancelled_on = db.Column(db.DateTime, nullable=True)
    orderItem = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    variation_id = db.Column(db.Integer, db.ForeignKey(
        'variation.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    variation_id = db.Column(db.Integer, db.ForeignKey(
        'variation.id'), nullable=False) #NULLABLETRUE
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Cart {self.id}>'


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    variation_id = db.Column(db.Integer, db.ForeignKey(
        'variation.id'), nullable=False)

    def __repr__(self):
        return f'<Wishlist {self.id}>'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Review {self.id}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Notification {self.id}>'


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(
        db.String(20), nullable=False, server_default='cash on delivery')
    transaction_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Payment {self.id}>'
