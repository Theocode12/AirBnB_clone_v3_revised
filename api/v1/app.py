#!/usr/bin/python3

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    storage.close()

@app.errorhandler(404)
def handles_error(error):
        return jsonify({'error':'Not found'}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
