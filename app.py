from flask import Flask, request, render_template
from flask_pymongo import PyMongo
# for api key 
import requests
# for env file 
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

# api key from env 
API_KEY = os.getenv('API_KEY')


import requests

categories = {
    "UI/UX": [ ],
    "Frontend": [ ],
    "Backend": [ ],
    "Career": [ ]
}

mongo.db.categories.insert_one(categories)

@app.route('/', methods =["GET","POST"])
def home():
    
    
    if request.method == "GET":

        return render_template('index.html')

    if request.method == "POST":
        # find the cateogry from db
        # grab the list of urls from ^
        # append the next url
        # update one with the list
        userCategory = request.form.get("link-category")

        new_link = {
            "url": request.form.get("add-link-modal-url"),
            "image_url": "",
            "title": "",
            "description": ""
        }
        
        users_url = new_link['url']
        url = f'https://api.linkpreview.net?key={API_KEY}&q={users_url}'
        response = requests.request("POST", url)
        item_json = response.json()

        new_link["image_url"] = item_json["image"]
        new_link["description"] = item_json["description"][0:110]
        new_link["title"] = item_json["title"]
        
        # mongo.db.new_link.drop()
        mongo.db.new_link.insert_one(new_link)

        if userCategory == mongo.db.categories.find(userCategory)

        ui_links = mongo.db.new_link.find({'category':'UI/UX'})
        context = {
            'ui_links' : ui_links
        }
        
        
        print(f'{new_link}')

    return render_template('display.html', **context)


@app.route('/templates/display.html', methods = ["POST"])
def allLinks():

    return None



if __name__ == '__main__':
    app.run(debug=True)
