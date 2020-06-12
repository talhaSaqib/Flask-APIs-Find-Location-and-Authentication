import os,sys
import importlib
root_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
#print "root_dir > ",root_dir

###############################################------MONGO DB CONNECTION------#######################################
from mongoengine import *
from DjangoCode.EC.models import *
from DjangoCode.django_mongo_utils import DjangoMongoUtils
#Django_Models_PATH = "DjangoCode.EC.models"  # change it to refer to any other app models (not using it now)


# IP = '206.189.69.43'
# Database_Name = 'eventchocolate'
# Username = 'fnb_admin'
# Password = '58c044e3c3bb717866-jk4321'

IP = 'localhost'
Database_Name = 'fnb'
Username = ''
Password = ''

Port = 27017

connect(Database_Name, 
		username=Username, password=Password,
		host=IP, port=Port,maxIdleTimeMS = 60000
)
#print importlib.import_module(Django_Models_PATH)
#######################################################################################################################
DB = DjangoMongoUtils(force_connect=False)