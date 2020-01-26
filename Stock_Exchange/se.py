from flask import Flask, jsonify, request
import random

app = Flask(__name__)

@app.route("/stocks")
def generate_numbers():
	no_stocks = int(request.args.get('no_stocks'))
	nums = []
	for i in range(no_stocks):
		num = random.randint(1,100)
		nums.append(num)

	return jsonify({"data":nums})

app.run(port=5001, debug=True)