from flask import Flask 
from flask import render_template
from flask import redirect
from flask import request
from flask_pymongo import PyMongo
import scrape_mars
from pymongo import MongoClient
import pymongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():

mars = mongo.db.mars.find_one()

return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():

# Run the scrape function
    mars = mongo.db.mars
    mars_web = scrape_mars.scrape_news()
    mars_web = scrape_mars.scrape_marsImage()
    mars_web = scrape_mars.scrape_marsTwitter()
    mars_web = scrape_mars.scrape_marsFacts()
    mars_web = scrape_mars.scrape_marsH1Cerberus()
    mars_web = scrape_mars.scrape_marsH2Schiaparelli()
    mars_web = scrape_mars.scrape_marsH3SyrtisMajor()
    mars_web = scrape_mars.scrape_marsH4VallesMarineris()
    
# Update the Mongo Database using update and upsert=True
    mars.update({}, mars_web, upsert=True)
    
# Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)