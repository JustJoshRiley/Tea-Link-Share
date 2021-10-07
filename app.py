from flask import Flask, request, render_template
from flask_pymongo import PyMongo
# for api key 
import requests
# for env file 
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:thisisSparta!@srv-captain--mongo/mydatabase?authSource=admin"
mongo = PyMongo(app)

# api key from env 
API_KEY = os.getenv('API_KEY')

import requests

categories_list = [
    {
        "name": "UI/UX",
        "data": [],
    },
    {
        "name": "Frontend",
        "data": [],
    },
    {
        "name": "Backend",
        "data": [],
    },
    {
        "name": "Career",
        "data": [],
    }
]

mongo.db.categories.drop()
mongo.db.categories.insert_many(categories_list)

@app.route('/', methods =["GET","POST"])
def home():
    if request.method == "GET":
        context = {
            'categories_list' : categories_list
        }
        return render_template('index.html', **context)

    if request.method == "POST":
        category_name =  str(request.form.get("link-category"))
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

        category = mongo.db.categories.find_one({"name" : category_name})

        data_list = category["data"]
        data_list.append(new_link)

        mongo.db.categories.update_one({"name": category_name}, {"$set": {"data": data_list}})
        variable = list(mongo.db.categories.find({}))
        context = {
            'categories_list': variable
        }
    return render_template('display.html', **context)



if __name__ == '__main__':
    app.run(host="localhost",debug=True)
