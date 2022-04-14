from flask import Flask

from top_rated_app.api.v1.views import api_v1_routes
from extensions import debug_toolbar, db

app = Flask(__name__)
# Register Blueprints
app.register_blueprint(api_v1_routes)

# Routes
@app.route("/")
def home():
    return {"success": True}

# Config file
app.config.from_object('config.settings')

# Extensions
def extensions(app):
    debug_toolbar.init_app(app)
    db.init_app(app)
    return None

extensions(app)

if __name__ == '__main__':
    app.run()
