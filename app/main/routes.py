from flask import render_template, request, flash, redirect, url_for, g
from flask_babel import get_locale
from flask_login import login_required

from app import db
from app.main import bp
from app.main.forms import EditProductForm
from app.models import Product, Category


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    categories = Category.query.all()
    all_products = Product.query.all()
    return render_template('index.html', title='Priser', categories=categories, products=all_products)


@bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='Om')


@bp.route('/products', methods=['GET'])
@login_required
def products():
    categories = Category.query.all()
    all_products = Product.query.all()
    return render_template('products.html', title='Produkter', categories=categories, products=all_products)


@bp.route('/product/<product_id>', methods=['GET', 'POST'])
@login_required
def product(product_id):
    prod = Product.query.filter_by(id=product_id).first_or_404()
    form = EditProductForm()
    if form.validate_on_submit():
        # product.id = id
        prod.name = form.name.data
        prod.url = form.url.data
        prod.maker = form.maker.data
        prod.protein_content = form.protein_content.data
        prod.weight = form.weight.data
        prod.tag_id = form.tag_id.data
        prod.category_id = form.category_id.data
        # db.session.add(product)
        db.session.commit()
        flash('Ändringar sparade.')
        return redirect(url_for('main.products'))
    elif request.method == 'GET':
        form.name.data = prod.name
        form.url.data = prod.url
        form.maker.data = prod.maker
        form.protein_content.data = prod.protein_content
        form.weight.data = prod.weight
        form.tag_id.data = prod.tag_id
        form.category_id.data = prod.category_id
    return render_template('edit_product.html', title='Ändra produkt', form=form)
