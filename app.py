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


links = [
    {"category":"UI/UX"},
    {"category": "Frontend"},
    {"category": "Backend"},
    {"category": "Career"},
    {"category": "Hiring"},

]
mongo.db.links.drop()

mongo.db.links.insert_many(links)

@app.route('/', methods =["GET","POST"])
def home():
    
    if request.method == "GET":
        all_of_links = mongo.db.links.find()

        context = {
            'links' : all_of_links,
        }

        return render_template('index.html', **context)

    if request.method == "POST":
        # mongo.db.links.drop()

        new_link = {
            "category" : request.form.get("link-category"),
            "url": request.form.get("add-link-modal-url")
        }
        
        # print(new_link['url'], 'users url')
        users_url = new_link['url']
        url = f'https://api.linkpreview.net?key={API_KEY}&q={users_url}'
        print(API_KEY)
        print(users_url)
        response = requests.request("POST", url)
        # print(response.text, 'response')



        mongo.db.links.update_one(new_link)


        # print(new_link, 'user validate')

        context = {
            "links" : links
        }
        
        for link in links:
            print(link)

    return render_template('displayLinkPreview.html', **context)



if __name__ == '__main__':
    app.run(debug=True)
