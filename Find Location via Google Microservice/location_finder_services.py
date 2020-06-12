"""
This file contains a service which gets CSV path and column name (having search queries) from
location_finder_via_google_api and return the locations of searched items by calling a 'google search' crawler
"""

__author__ = "Talha Saqib"

# Local Imports
import change_root_dir
from configurator import Configurator
from funnelbeam.google_crawler.google_wrapper import GoogleWrapper
from funnelbeam.web_crawler.get_contacts_info.contact_extractor import ContactExtractor
from funnelbeam.utils.address_utilities.addr_cleaner import AddrCleaner

# Third-party Imports
from nameko.rpc import rpc
import pandas as pd

config = Configurator()
logger = config.set_logger()
logger.info(change_root_dir.root_dir)

class LocationFinderViaGoogle:
    name = "location_finder"

    @rpc
    def location_finder_via_google_csv(self, csv_path, column_name):
        try:
            logger.info("INSIDE: location_finder_via_google_csv() SERVICE")

            df = pd.read_csv(csv_path)
            search_items_as_df = df[column_name]
            search_items_list = search_items_as_df.tolist()

            # Calling Google crawler to search locations for search_items
            gw = GoogleWrapper(proxy="", retries = 3, save_html_file = True)

            logger.info("INSIDE: Initiating Web Crawler")
            response = [gw.get_company_info(search_item) for search_item in search_items_list]

            return response

        except Exception as e:
            logger.error("Error = {}".format(e))
            response = {"Error: ": e}
            return response

    @rpc
    def location_finder_via_google(self, company_name):
        try:
            logger.info("INSIDE: location_finder_via_google() SERVICE")

            gw = GoogleWrapper(proxy="", retries=3, save_html_file=True)

            logger.info("INSIDE: Initiating Web Crawler")
            response = gw.get_company_info(company_name)

            return response

        except Exception as e:
            logger.error("Error = {}".format(e))
            response = {"Error: ": e}
            return response

    @rpc
    def location_finder_via_url(self, company_url):
        try:
            logger.info("INSIDE: location_finder_via_url() SERVICE")

            contact_extractor = ContactExtractor(domain_validator=False, parallel_run=True, do_address_find=True,
                                                 main_page_scrape_only=False, scrape_first_level=True)
            contacts_dict = contact_extractor.extract_contact_details(url=company_url)

            addresses_list = contacts_dict.get("addresses")
            if addresses_list:
               # cleaning address and extracting country, state and city
                addr_cleaner = AddrCleaner()
                cleaned_addresses = [addr_cleaner.clean_us_address(addr) for addr in addresses_list]

                response = [cleaned_addresses, addresses_list, contacts_dict]
            else:
                response = contacts_dict    # change it with 'None'

            return response

        except Exception as e:
            logger.error("Error = {}".format(e))
            response = {"Error: ": e}
            return response

