from flask import Flask
from flask_celery import make_celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL']='ampq://localhost//'
app.config['CELERY_BACKEND']='db+mysql://root:Root@123@localhost/celery'

celery = make_celery(app)

@app.route('/process/<name>')
def process(name):
    return name

if __name__ == '__main__':
    app.run(debug=True)