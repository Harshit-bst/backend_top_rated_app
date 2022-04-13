from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from sqlalchemy import desc

from extensions import debug_toolbar, db
from top_rated_app.models import AndroidApp

app = Flask(__name__)

def get_app_json_formatted_data(apps_data, category):
    result = []
    for app in apps_data:
        image = app.find("img", attrs={"class": ["T75of", "QNCnCf"]}).attrs['data-src']
        name = app.find("div", attrs={"class": ["WsMG1c", "nnK0zc"]}).text
        pkg = app.find("div", attrs={"class": ["WsMG1c", "nnK0zc"]}).parent.attrs["href"].split("id=")[-1]
        corporation = app.find("div", attrs={"class": ["KoLSrc"]}).text
        data = {
            "image_url": image,
            "name": name,
            "corporation": corporation,
            "pkg": pkg,
            "category": category,
        }
        android_app_obj = AndroidApp.query.filter_by(pkg=pkg).first()
        if not android_app_obj:
            db.session.add(AndroidApp(**data))
@app.route("/")
def home():
    return {"success": True}


@app.route("/api/v1/get-all-apps")
def get_all_apps():
    all_apps = AndroidApp.query.order_by(desc(AndroidApp.created_on)).all()
    response_data = {}
    for app in all_apps:
        data = {
            "image_url": app.image_url,
            "name": app.name,
            "corporation": app.corporation,
            "pkg": app.pkg
        }
        category = app.category
        if response_data.get(category):
            response_data[category].append(data)
        else:
            response_data[category] = [data]
    response = jsonify({"data": response_data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/v1/save-new-apps')
def save_new_apps():  # put application's code here
    response = requests.get("https://play.google.com/store/apps/top")
    soup = BeautifulSoup(response.content, "html5lib")
    top_free_apps, top_paid_apps, top_grossing_apps, top_free_games, top_paid_games, top_grossing_games = list(soup.findAll("div", attrs={"class": ['ZmHEEd', 'fLyRuc']}))
    get_app_json_formatted_data(top_free_apps.children, "top_free_apps")
    get_app_json_formatted_data(top_paid_apps.children, "top_paid_apps")
    get_app_json_formatted_data(top_grossing_apps.children, "top_grossing_apps")
    get_app_json_formatted_data(top_free_games.children, "top_free_games")
    get_app_json_formatted_data(top_paid_games.children, "top_paid_games")
    get_app_json_formatted_data(top_grossing_games.children, "top_grossing_games")
    db.session.commit()
    response = jsonify({"success": True})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# def get_app_detail_json_formatted_data(data):
#     response = {
#
#     }
#     icon = data.find("img", attrs={"alt": "Cover art"})
#     icon = data.find("img", attrs={"alt": "Cover art"})
#     icon = data.find("img", attrs={"alt": "Cover art"})
#     icon = data.find("img", attrs={"alt": "Cover art"})
#     icon = data.find("img", attrs={"alt": "Cover art"})
#     icon = data.find("img", attrs={"alt": "Cover art"})


@app.route('/api/v1/apps/details', methods=['GET'])
def get_app_details():
    id = request.args.get("id")
    response = requests.get(f"https://play.google.com/store/apps/details?id={id}")
    soup = BeautifulSoup(response.content, "html5lib")
    response_data = soup.find("c-wiz", attrs={"class": ["zQTmif", "SSPGKf", "I3xX3c", "drrice"]})
    # response_data = get_app_detail_json_formatted_data(response_data)
    response = jsonify({"data": str(response_data)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.config.from_object('config.settings')
app.config.from_pyfile('settings.py', silent=True)


def extensions(app):
    debug_toolbar.init_app(app)
    db.init_app(app)
    return None

extensions(app)
if __name__ == '__main__':
    app.run()
