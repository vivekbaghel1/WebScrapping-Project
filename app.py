from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Define app
app = Flask(__name__)

# Establish Mongo Connections
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Routes 
# Home Route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


# Scrape Route
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )

    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)