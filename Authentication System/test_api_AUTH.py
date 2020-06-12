"""
Test API
"""

__author__ = "Talha Saqib"

# Local imports
import change_root_dir
from configurator import Configurator
from FlaskAPI.fnb_flask_auth.auths import *
from FlaskAPI.connection import *

# Third-party imports
from flask import Flask, jsonify, g

app = Flask(__name__)
config = Configurator()
logger = config.set_logger()


@app.route("/testing_token", methods=["GET"])
@auth.login_required
def testing():
    return "TOKEN AUTH IS WORKING"


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', use_reloader=True,
            port=8888)
