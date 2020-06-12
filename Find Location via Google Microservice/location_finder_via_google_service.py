"""
This file contains a service which gets CSV path and column name (having search queries) from
location_finder_via_google_api and return the locations of searched items by calling a 'google search' crawler
"""

__author__ = "Talha Saqib"

# Local Imports
import change_root_dir
from configurator import Configurator
from funnelbeam.google_crawler.google_wrapper import GoogleWrapper
import json

# Third-party Imports
from nameko.rpc import rpc
import pandas as pd

config = Configurator()
logger = config.set_logger()
logger.info(change_root_dir.root_dir)

class LocationFinderViaGoogle:
    name = "location_finder_via_google"

    @rpc
    def location_finder_via_google(self, csv_path, column_name):
        try:
            logger.info("INSIDE: location_finder_via_google")

            df = pd.read_csv(csv_path)
            # search_items_as_df = df[column_name].head(10)       #Remove this line, this is for testing
            search_items_as_df = df[column_name]
            search_items_list = search_items_as_df.tolist()

            # Calling Google crawler to search locations for search_items
            gw = GoogleWrapper(proxy="", retries = 3, save_html_file = True)

            logger.info("INSIDE: Inititaing Web Crawler")
            response = [gw.get_company_info(search_item) for search_item in search_items_list]

            return response

        except Exception as e:
            logger.error("Error = {}".format(e))
            response = {"Error: ": e}
            return response

