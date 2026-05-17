import json

from flask import Flask, render_template, request, session, flash, redirect, url_for
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_flower_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
    return flowers

def load_addon_data():
    with open('data/addon.json') as file:
        addons = json.load(file)
    return addons

@app.route('/')
def index():
    flowers = load_flower_data()
    addon = load_addon_data()
    return render_template('index.html', flower=flowers, addon=addons)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower']
    quantity = int(request.form['quantity'])
    flowers, addons = load_data()
    cart = session.get('cart', {})

    if flower not in flowers:
        flash("Invalid Flower Selected.")
        return redirect(url_for('home'))
    
    if flower in cart:
        cart[flower]['quantity'] += quantity
    else:
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }
    
    session['cart'] = cart
    session.modified = True
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/invoice')
def invoice():
    return render_template('invoice.html')

@app.route('/orders')
def order_history():
    return render_template('order_history.html')

if __name__ == '__main__':
    app.run(debug=True)