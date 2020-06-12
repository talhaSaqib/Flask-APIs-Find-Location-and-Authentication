"""
This file implements a FlaskAPI that takes a company name, website link and
then via its respective service, returns the address from a contact page.
"""

__author__ = "Talha Saqib"

# Local Imports
from configurator import Configurator

# Third-party imports
from flask import Flask, jsonify, request
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
CONFIG = {'AMQP_URI': "amqp://guest:guest@0.0.0.0"}
config = Configurator()
logger = config.set_logger()

@app.route("/location/find_via_url", methods=["GET"])
def location_finder_via_url():
    try:
        logger.info("INSIDE: location_finder_via_website() API")

        company_url = request.args.get('company_url')

        if company_url:
            with ClusterRpcProxy(CONFIG) as rpc:
                logger.info("INSIDE: ClusterRpcProxy(CONFIG)")

                # Using Service on address present in CONFIG
                service_response = rpc.location_finder\
                    .location_finder_via_url(company_url)

                response = {"Response": service_response}
                return jsonify(response)
        else:
            response = {"Response": "Company Url is NULL. Please enter a valid input."}
            return jsonify(response)

    except Exception as e:
        logger.error("Error = {}".format(e))
        response = {"Error: ": e}
        return jsonify(response)

if __name__ == "__main__":
    app.run(debug = True, threaded = True, host = '0.0.0.0', use_reloader = True, port = 8888)