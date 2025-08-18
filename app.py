from flask import Flask, redirect, url_for, render_template
import pymysql
import cryptography
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HARD TO GUESS STRING'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://app:Pierreevan@localhost:3306/e_commerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Models

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(34), index=True)
    price = db.Column(db.Integer())
    image_url = db.Column(db.String(34), index=True)

@app.route('/', methods=['GET'])
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/checkout/<book_id>', methods=['GET'])
def checkout(book_id):
    product = Product.query.filter_by(id=book_id).first()
    return render_template('checkout.html', product=product)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
