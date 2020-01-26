from celery import Celery 
import time
app = Celery('tasks',broker='amqp://localhost//',result_backend='db+mysql://root:Root@123@localhost/celery')

@app.task
def reverse(string):
    time.sleep(10)
    return string[::-1]