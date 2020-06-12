"""
This file contains method that calls a function to generate API authentication token and then returns that token.
"""

__author__  = "Talha Saqib"

# Local imports
import change_root_dir
from configurator import Configurator
from FlaskAPI.fnb_flask_auth.auths import *

app = Flask(__name__)
config = Configurator()
logger = config.set_logger()

@app.route("/get_api_auth_token", methods=["GET"])
@auth.login_required
def get_token():
    try:
        token = g.user.generate_auth_token()

        response = {'API Token': token}
        return jsonify(response)

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', use_reloader=True,
			port=8888)


