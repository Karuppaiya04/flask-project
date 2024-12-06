from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

# Routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.image
    })
    session.modified = True
    flash(f"{product.name} added to cart!")
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)
        flash("Order placed successfully!")
        return redirect(url_for('home'))
    return render_template('checkout.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image']
        description = request.form['description']

        new_product = Product(name=name, price=price, image=image, description=description)
        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully!")
        return redirect(url_for('home'))

    return render_template('add_product.html')

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)
