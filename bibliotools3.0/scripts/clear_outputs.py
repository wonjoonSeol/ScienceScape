import shutil
import os

dir = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(os.path.join(dir, "../Result")):
    shutil.rmtree('../Result')
