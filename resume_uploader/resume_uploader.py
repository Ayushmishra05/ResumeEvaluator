from wtforms import FileField, SubmitField 
from flask import Flask , render_template , flash, redirect, url_for, request
from flask_wtf import FlaskForm
from dotenv import load_dotenv 
from werkzeug.utils import secure_filename
from flask_wtf.file import FileAllowed
import os 
import uuid 
import boto3 
import io 
import requests
load_dotenv() 




s3_client = boto3.client('s3') 
bucket_name = "resumesbyevaluator" 


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
app = Flask(__name__ , template_folder=os.path.join(root_dir, "templates")) 

app.config["SECRET_KEY"] = os.environ['skey'] 
# print(os.environ['skey'])
URL = os.getenv("backend_url" , "http://localhost:8000")

class UploadFile(FlaskForm):
    file = FileField("Upload file" , validators = [FileAllowed(['pdf'])]) 
    submit = SubmitField("Submit file")


@app.route("/" , methods = ['GET' , 'POST']) 
def index():
    form = UploadFile()
    message = None

    if form.validate_on_submit():
        uploaded_file = form.file.data 
        file_name = secure_filename(uploaded_file.filename) 
        secured_name = f"{uuid.uuid4().hex}_{file_name}"
        try:
            resume_file = io.BytesIO(uploaded_file.read())
            s3_client.upload_fileobj(resume_file , Key = secured_name , Bucket = bucket_name) 
            print("File Uploaded in S3")
            message = "Your File Was Uploaded Successfully"
            fileid = f"https://resumesbyevaluator.s3.us-east-1.amazonaws.com/{secured_name}"
            data = {
                "url" : fileid , 
                "description" : "The Job is for Software Developer, capable of having Devops skills, Development skills is manageable, skills including Kubernetes, docker and other devops skills"
            }
            response = requests.post(url = URL  , json=data)
            if response.status_code == 200:
                print("File was Sent") 
            else:
                print("File wasn't sent" )
        except Exception as e:
            print("Couldn't Upload into S3 , error " , e)
            message = "Your File Was not uploaded, Try it again"
            
        
    return render_template("index.html", form = form , message = message) 

if __name__ == "__main__":
    app.run("0.0.0.0" , port = 5000) 
