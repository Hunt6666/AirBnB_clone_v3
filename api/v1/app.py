#!/usr/bin/python3
"""
Starting an API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)

@app.teardown_appcontext
def close(content):
    """
    handling teardowns
    """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
