from flask import Flask , request, jsonify
import requests 
from resumtotext import ResumeToText
from mongo_upload import upload_in_mongo
app = Flask(__name__) 

@app.route("/" , methods = ['POST'])
def index():
    data = request.get_json() 
    url = data.get("url")
    desc = data.get("description") 
    rtt = ResumeToText(url, desc) 
    dict_obj = rtt.analyse_overall()  
    dict_obj['url'] = url 
    dict_obj['desc'] = desc 
    status = upload_in_mongo(dict_obj) 
    if status:
        return jsonify({"message": "File uploaded and analyzed successfully"}), 200
    else:
        return jsonify({"error": "Failed to upload to MongoDB"}), 500

    
if __name__ == "__main__":
    app.run(port = 8000)
    





