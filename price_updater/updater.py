import datetime
import os

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Price, Product
from config import Config
from price_updater.parsers import parse

basedir = os.path.abspath(os.path.dirname(__file__))


class Updater:
    def __init__(self):
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __repr__(self):
        return '<Updater>'

    # def create_database(self):
    #   Base.metadata.create_all(self.engine)

    # def drop_database(self):
    #   Base.metadata.drop_all(self.engine)

    def update(self):
        i = 0
        for p in self.get_all_products():
            headers = {'user-agent': 'my-app/0.0.1'}
            try:
                response = requests.get(p.url, headers=headers)
            except RequestException:
                print('Could not connect to {}, moving on.'.format(p.url))
                continue
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                price = parse(p, soup)
                new_price = Price(product_id=p.id, price=price, date=datetime.datetime.now())
                self.session.add(new_price)
                # self.add(new_price)
                i = i + 1
            else:
                print('Got status {} from web page'.format(response.status_code))
        if i > 0:
            self.session.commit()
        return i

    def add(self, db_object):
        self.session.add(db_object)
        self.session.commit()

    def get_all_products(self):
        return self.session.query(Product).all()

    def get_all_prices(self, product):
        return self.session.query(Price).filter_by(product_id=product.id)

    def get_latest_price(self, product):
        return self.session.query(Price).order_by(Price.date.desc()).filter_by(product_id=product.id).first()


if __name__ == "__main__":
    print("Updating prices...")
    updater = Updater()
    updated_prices = updater.update()
    print("Done, updated {} prices".format(updated_prices))
