from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route('/')
def index():
	mars_data = mongo.db.mars_data.find_one()
	return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
	mars_data = mongo.db.mars_data
	mars_rollup = scrape_mars.scrape()
	mars_data.insert(rollup_dict)

	return 'Scrape complete'

if __name__ == '__main__':
	app.run(debug=True)