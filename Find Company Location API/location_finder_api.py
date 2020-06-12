"""
This file implements a Flask API to find a company's location given its domain and name.
"""

__author__ = "Talha Saqib"

# Local imports
import change_root_dir
from configurator import Configurator
from funnelbeam.utils.custom_validators.domain_validator import DomainValidator
import funnelbeam.utils.data_filtering_utils as data_filter

# Third-party imports
from flask import Flask, jsonify, request

app = Flask(__name__)
config = Configurator()
logger = config.set_logger()

@app.route("/find_company_location", methods=["GET"])
def find_company_location():
    try:
        company_name = request.args.get('company_name')
        domain = request.args.get('domain')

        domain_validator = DomainValidator()

        # Location finding via company domain
        location_info = domain_validator.get_domain_location_info(domain)

        if location_info.get("country"):
            logger.info("Location Retrieved via Domain")

            location = location_info.get("country")
            location_src = {"source":"Domain", "location":location}

            return jsonify(location_src)
        else:
            # Location finding via company name
            location = data_filter.get_company_location_from_company_name(company_name)

            response = {"source":"Company Name", 'location':location}
            return jsonify(response)

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', use_reloader=True,
			port=8888)
