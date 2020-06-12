"""
This file changes the root directory to 'fnb-backend'.

Simply import this file to make the code below work.

Always import it before importing any FunnelBeam module.
"""

__author__ = "Talha Saqib"

# Local Imports
import os
import sys
import re

# Changing root directory to 'fnb-backend'
root_dir = os.path.abspath(__file__)
while not re.search("fnb-backend$", root_dir):
    root_dir = os.path.dirname(root_dir)

sys.path.append(root_dir)