# this is where we are using Flask and Mogo to begin creating a web app
# importing our tools
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# setting up up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# setting up our Flask routes: 
# one for the main HTML page everyone will view when visiting the web app, and 
# one to actually scrape new data using the code we've written
# mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, 
# which we will create when we convert our Jupyter scraping code to Python Script

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# setting up next function for our scraping route
# This route will be the "button" of the web application
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# final bit of code we need for Flask is to tell it to run
if __name__ == "__main__":
   app.run()