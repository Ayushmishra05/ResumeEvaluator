from flask import Flask , request, jsonify
import requests 
from resume_process.resumtotext import ResumeToText
from resume_process.mongo_upload import upload_in_mongo
from utils.send_mail import notify_candidate
import json
app = Flask(__name__) 

@app.route("/" , methods = ['POST'])
def index():
    data = request.get_json() 
    desc = data.get("description")  
    job = data.get("role")
    email = data.get('email')
    name = data.get("name")
    company = data.get("company")
    rtt = ResumeToText(job , desc) 
    dict_obj , insights = rtt.analyse_overall()  
    dict_obj['desc'] = desc 
    dict_obj['role'] = job 
    dict_obj['email'] = email
    score = dict_obj['Score']
    reason = dict_obj['Reason'] 
    status = upload_in_mongo(dict_obj) 
    if status:
        notify_candidate(name , job , score, email , company , insights , reason)
        return jsonify({"message": "File uploaded and analyzed successfully"}), 200 
    else:
        return jsonify({"error": "Failed to upload to MongoDB"}), 500

    
if __name__ == "__main__":
    app.run(port = 8000)
    





