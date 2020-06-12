"""
This file implements a FlaskAPI that takes a company name and
then send it to location_finder_via_google_service to ultimately get the locations of that company.
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

@app.route("/location/find_via_google", methods=["GET"])
def location_finder_via_google():
    try:
        logger.info("INSIDE: location_finder_via_google() API")

        company_name = request.args.get('company_name')

        if company_name:
            with ClusterRpcProxy(CONFIG) as rpc:
                logger.info("INSIDE: ClusterRpcProxy(CONFIG)")

                # Using Service on address present in CONFIG
                service_response = rpc.location_finder\
                    .location_finder_via_google(company_name)

                response = {"Response": service_response}
                return jsonify(response)
        else:
            response = {"Response": "Company Name is NULL. Please enter a valid input."}
            return jsonify(response)


    except Exception as e:
        logger.error("Error = {}".format(e))
        response = {"Error: ": e}
        return jsonify(response)

if __name__ == "__main__":
    app.run(debug = True, threaded = True, host = '0.0.0.0', use_reloader = True, port = 8888)