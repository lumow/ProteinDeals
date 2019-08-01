import os

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

from app import db, login


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    maker = db.Column(db.String)
    weight = db.Column(db.Integer)
    protein_content = db.Column(db.Integer)
    url = db.Column(db.String)
    tag_id = db.Column(db.String)
    price = db.relationship('Price', backref='product', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), index=True)

    def get_latest_price(self):
        return Price.query.order_by(Price.date.desc()).filter_by(product_id=self.id).first()

    def __repr__(self):
        return '<Product id {}, name {}, maker {}, url {}>'.format(self.id, self.name, self.maker, self.url)


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Numeric)
    date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Price id {}, product_id {}, price {}, date {}>'.format(self.id, self.product_id, self.price, self.date)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
