"""
This file changes the root directory to 'fnb-backend', so imports can be done.

Simply import this file to make the code below work

Always import it before importing any FunnelBeam module
"""

__author__ = "Talha Saqib"

# Local Imports
import os
import sys

# Changing root directory to 'fnb-backend'
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)