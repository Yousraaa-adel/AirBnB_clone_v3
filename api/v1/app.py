#!/usr/bin/python3
"""_summary_
"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, threaded=True)