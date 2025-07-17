from flask import Flask , request, jsonify
import requests 
from resume_process.resumtotext import ResumeToText
from resume_process.mongo_upload import upload_in_mongo
from utils import send_mail
import json
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
        # file_path = "<|PATH|>" 
        # with open(file_path , 'r') as fp:
        #     data = json.load(fp)
        send_mail(data['email'])
        return jsonify({"message": "File uploaded and analyzed successfully"}), 200 
    else:
        return jsonify({"error": "Failed to upload to MongoDB"}), 500

    
if __name__ == "__main__":
    app.run(port = 8000)
    





