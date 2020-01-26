import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler


def get_stocks():
	no_stocks = 100
	r = requests.get("http://localhost:5001/stocks?no_stocks={}".format(no_stocks))
	with open('file') as f:
		f.write(r.text)
	return

scheduler = BackgroundScheduler()
scheduler.add_job(get_stocks, 'interval', seconds=20)#, args=[datetime.utcnow()])
scheduler.start()