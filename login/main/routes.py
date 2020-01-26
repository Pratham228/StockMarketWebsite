from flask import render_template, request, Blueprint,current_app, jsonify
from login.models import Post
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import requests
#from login import STOCK_VALUE

main = Blueprint('main',__name__)

def get_call():
    r = requests.get("http://localhost:5001/stocks?no_stocks=100").json()
    #print(r['data'][0])
    return r

@main.route('/')
@main.route('/home')
def home():
    
    r= get_call()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=get_call, trigger="interval", seconds=3)
    # scheduler.start()
    # print(r)
    # # Shut down the scheduler when exiting the app
    # atexit.register(lambda: scheduler.shutdown())
    
    # current_app.logger.info("Processing home request")
    #print(STOCK_VALUE)
    posts = Post.query.all() 
    return render_template('home.html',posts=posts,data=r)

@main.route('/about')
def about():
    return render_template('about.html',title='About')

@main.route('/refresh_data')
def refresh_data():
    
    r= get_call()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=get_call, trigger="interval", seconds=3)
    # scheduler.start()
    # print(r)
    # # Shut down the scheduler when exiting the app
    # atexit.register(lambda: scheduler.shutdown())
    
    # current_app.logger.info("Processing home request")
    #print(STOCK_VALUE)
    return jsonify(r)