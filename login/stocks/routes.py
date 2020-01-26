from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from login import db, cache, q
from login.models import BuyStocks, Stock, BankAccount,SellStocks, UserStocks
from login.stocks.forms import BuyStocksForm, SellStocksForm, TransferMoneyForm, PlanScheduleForm, StockForm
import schedule
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
#from flask.ext.restless import APIManager


stocks = Blueprint('stocks',__name__)

@stocks.route('/buystocks', methods=['GET','POST'])
#@cache.cached(timeout=50)
@login_required
def buy_stocks():
    form = BuyStocksForm()
    if form.validate_on_submit():
        cache.clear()

        stock = Stock.query.filter_by(ticker_symbol=form.ticker_symbol.data).first()
        buy_stock = BuyStocks(ticker_symbol=form.ticker_symbol.data, user_id=current_user.id,buy_price=stock.price,no_of_stocks=form.no_of_stocks.data)
        db.session.add(buy_stock)
        user_stock_query = UserStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).first()
        if user_stock_query is None:
            user_stock = UserStocks(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id,no_of_stocks=form.no_of_stocks.data,company_name=stock.company_name)
            db.session.add(user_stock)
        else:
            new_no_of_stocks = (user_stock_query.no_of_stocks + form.no_of_stocks.data)
            UserStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).update({'no_of_stocks':new_no_of_stocks})
        bank_account1 = BankAccount.query.filter_by(bank_account_no=form.bank_account_no.data.bank_account_no,user_id=current_user.id).first()
        new_amount= bank_account1.amount-(stock.price * form.no_of_stocks.data)
        BankAccount.query.filter_by(user_id=current_user.id, bank_account_no=form.bank_account_no.data.bank_account_no).update({'amount':new_amount})
        db.session.commit()
        
        flash('You have successfully bought the stock','success')
        
        return redirect(url_for('main.home'))
    return render_template('buystocks.html',title='Buy Stocks',form = form, legend = 'Buy Stocks')

@stocks.route('/sellstocks',methods=['GET','POST'])
#@cache.cached(timeout=50)
@login_required
def sell_stocks():
    form = SellStocksForm()
    if form.validate_on_submit():
        cache.clear()
        stock = Stock.query.filter_by(ticker_symbol=form.ticker_symbol.data).first()
        # buy_stock_price= BuyStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).first()
        # sell_stock = SellStocks(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id,buy_price=buy_stock_price.buy_price,selling_price=stock.price,no_of_stocks=form.no_of_stocks.data)
        sell_stock = SellStocks(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id,selling_price=stock.price,no_of_stocks=form.no_of_stocks.data)
        db.session.add(sell_stock)
        bank_account1 = BankAccount.query.filter_by(bank_account_no=form.bank_account_no.data.bank_account_no,user_id=current_user.id).first()
        new_amount= bank_account1.amount+(stock.price * form.no_of_stocks.data)
        BankAccount.query.filter_by(user_id=current_user.id, bank_account_no=form.bank_account_no.data.bank_account_no).update({'amount':new_amount})
        BuyStocks.query.filter_by(user_id=current_user.id,ticker_symbol=form.ticker_symbol.data).delete()
        user_stock_query = UserStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).first()
        new_no_of_stocks = (user_stock_query.no_of_stocks - form.no_of_stocks.data)
        UserStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).update({'no_of_stocks':new_no_of_stocks})
        db.session.commit()
        flash('You have successfully sold the stock','success')
        return redirect(url_for('main.home'))
    return render_template('sellstocks.html',title='Sell Stocks',form = form, legend = 'Sell Stocks')

@stocks.route('/mystocks')
@cache.cached(timeout=100)
@login_required
def mystocks():
    var = cache.get('mystocks')
    #print(var)
    cache.clear()    
    if var is None:
        print("Cache Miss")
        # cache.set('mystocks',var,timeout=100)
    else:
        print("Cache Hit")
    
    stocks = UserStocks.query.filter_by(user_id=current_user.id)
    # stocks1 = stocks.query.filter_by()
    return render_template('mystocks.html',stocks=stocks, legend = 'My Stocks')

@stocks.route('/transfermoney',methods=['GET','POST'])
#@cache.cached(timeout=50)
@login_required
def transfer_money():
    form = TransferMoneyForm()
    print("Form rendered")
    if form.validate_on_submit():
        
        bank_account1 = BankAccount.query.filter_by(bank_account_no=form.bank_account_no1.data.bank_account_no,user_id=current_user.id).first()
        bank_account2 = BankAccount.query.filter_by(bank_account_no=form.bank_account_no2.data.bank_account_no,user_id=current_user.id).first()
        new_amount_for1= (bank_account1.amount - form.amount_to_transfer.data)
        new_amount_for2= (bank_account2.amount + form.amount_to_transfer.data)
        BankAccount.query.filter_by(user_id=current_user.id, bank_account_no=bank_account1.bank_account_no).update({'amount':new_amount_for1})  
        BankAccount.query.filter_by(user_id=current_user.id, bank_account_no=bank_account2.bank_account_no).update({'amount':new_amount_for2})
        db.session.commit()
        flash('You have successfully transferred the money!','success')
        return redirect(url_for('main.home'))
    return render_template('transfermoney.html',title='Transfer Money',form = form, legend = 'Transfer Money')

def call_pending():
        schedule.run_pending()
        time.sleep(1)
    

@stocks.route('/planschedule',methods=['GET','POST'])
#@cache.cached(timeout=50)
@login_required
def plan_schedule():
    form = PlanScheduleForm()
    
    def buy():
        print("Scheduled stock has been bought!")
        ##Call the logic for buying scheduled stock
        # stock = Stock.query.filter_by(ticker_symbol=form.ticker_symbol.data).first()
        # buy_stock = BuyStocks(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id,buy_price=stock.price,no_of_stocks=form.no_of_stocks.data)
        # db.session.add(buy_stock)
        # user_stock_query = UserStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).first()
        # if user_stock_query is None:
        #     user_stock = UserStocks(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id,no_of_stocks=form.no_of_stocks.data)
        #     db.session.add(user_stock)
        # else:
        #     new_no_of_stocks = (user_stock_query.no_of_stocks + form.no_of_stocks.data)
        #     UserStocks.query.filter_by(ticker_symbol=form.ticker_symbol.data,user_id=current_user.id).update({'no_of_stocks':new_no_of_stocks})
        # bank_account1 = BankAccount.query.filter_by(bank_account_no=form.bank_account_no.data.bank_account_no,user_id=current_user.id).first()
        # new_amount= bank_account1.amount-(stock.price * form.no_of_stocks.data)
        # BankAccount.query.filter_by(user_id=current_user.id, bank_account_no=form.bank_account_no.data.bank_account_no).update({'amount':new_amount})
        # db.session.commit()

        
    if form.validate_on_submit():
        #schedule.every().friday.at("00:46").do(buy) 
        schedule.every(2).minutes.do(buy)    
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=call_pending, trigger="interval", seconds=3)
        scheduler.start()
        #print("scheduler started")
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())


        flash('You have successfully planned the buy schedule!','success')
        return redirect(url_for('main.home'))
        
   
    
    return render_template('planschedule.html',title='Plan Schedule',form = form, legend = 'Plan Schedule')

 
# @login_required
# @stocks.route('/buy-stocks')
# def buy_stocks1():
#     #user = current_user
#     #db_object
#     list_of_stocks = []
#     return jsonify({"list_of_stocks":list_of_stocks})

@login_required
@stocks.route('/get_stock_tickers')
@cache.cached(timeout=50)
def get_stock_tickers():
    stocks = Stock.query.all()
    list_of_stocks=list()
    for stock in stocks:
        list_of_stocks.append(stock.ticker_symbol)

    return jsonify({"list_of_stock_tickers":list_of_stocks})

@login_required
@stocks.route('/get_user_bank_accounts')
@cache.cached(timeout=50)
def get_user_bank_account():
    bank_accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
    list_of_accounts=list()
    for account in bank_accounts:
        list_of_accounts.append(account.bank_account_no)

    return jsonify({"list_of_stocks":list_of_accounts})


@login_required
@stocks.route('/get_stocks')
@cache.cached(timeout=50)
def get_stocks():
    stocks = Stock.query.all()
    list_of_stocks = list()
    for stock in stocks:
        list_of_stocks.append(stock)

    return jsonify({"":list_of_stocks})

