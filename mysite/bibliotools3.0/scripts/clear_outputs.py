import shutil
import os

"""
This script removes the Result (output from running_scripts.py) folder from the source directory,
and all its contents.
"""

dir = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(os.path.join(dir, "../Result")):
    shutil.rmtree('../Result')
