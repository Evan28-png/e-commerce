from flask import Flask, redirect, url_for, render_template
import pymysql
import cryptography
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')   
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET')
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/e_commerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Enable Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'E-commerce app with monitoring', version='1.0.0')

#Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    price = db.Column(db.Integer())
    image_url = db.Column(db.String(255), index=True)

@app.route('/', methods=['GET'])
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/checkout/<book_id>', methods=['GET'])
def checkout(book_id):
    product = Product.query.filter_by(id=book_id).first()
    return render_template('checkout.html', product=product)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
