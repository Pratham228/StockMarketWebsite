
from flask import current_app
from login import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    address = db.Column(db.String(50),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='user',lazy=True)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}',{self.email},'{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    author = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) 
    def __repr__(self):
        return f"Post('{self.name}','{self.author}')"

class BankAccount(db.Model):
    bank_account_no = db.Column(db.String(20),primary_key=True)
    routing_number = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return f"BankAccount('{self.bank_account_no}','{self.user_id}')"

class Stock(db.Model):
    ticker_symbol = db.Column(db.String(20),primary_key=True)
    company_name = db.Column(db.String(20),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return f"Stock('{self.ticker_symbol}','{self.company_name}','{self.price}')"

class BuyStocks(db.Model):
    ticker_symbol = db.Column(db.String(20),db.ForeignKey('stock.ticker_symbol'),primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
    buy_price = db.Column(db.Integer,nullable=False)
    no_of_stocks = db.Column(db.Integer,nullable=False)
    buy_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,primary_key=True)

class SellStocks(db.Model):
    ticker_symbol = db.Column(db.String(20),db.ForeignKey('stock.ticker_symbol'),primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
    selling_price =db.Column(db.Integer,nullable=False)
    no_of_stocks = db.Column(db.Integer,nullable=False)
    sell_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,primary_key=True)

class UserStocks(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
    ticker_symbol = db.Column(db.String(20),db.ForeignKey('stock.ticker_symbol'),primary_key=True)
    no_of_stocks = db.Column(db.Integer,nullable=False)
    company_name = db.Column(db.String(20))
