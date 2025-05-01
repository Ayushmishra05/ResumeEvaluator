
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os 
from dotenv import load_dotenv 
load_dotenv()
uname = os.environ["uname"]
password = os.environ["password"]
uri = f"mongodb+srv://{uname}:{password}@resume.ygr1ier.mongodb.net/?retryWrites=true&w=majority&appName=Resume" 

def upload_in_mongo(data):
    client = MongoClient(uri)
    db = client["MetricLabsDB"] 
    collection = db["Resume"] 
    result = collection.insert_one(data)
    doc = collection.find_one({"_id": result.inserted_id})
    client.close()
    if doc:
        return True 
    else :
        return False  


