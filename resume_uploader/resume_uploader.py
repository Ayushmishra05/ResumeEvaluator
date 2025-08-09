"""Resume Uploader 
"""

from wtforms import FileField, SubmitField 
from flask import Flask , render_template , flash, redirect, url_for, request
from flask_wtf import FlaskForm
from dotenv import load_dotenv 
from werkzeug.utils import secure_filename
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired, Email
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
    email = StringField("Email", validators=[DataRequired(), Email()]) 
    job_role = StringField("Job Role" , validators=[DataRequired()])
    job_description = StringField("Job Description")
    company = StringField("Company" , validators=[DataRequired()])
    name = StringField("name" , validators=[DataRequired()])
    submit = SubmitField("Submit file")



@app.route("/" , methods = ['GET' , 'POST']) 
def index():
    form = UploadFile()
    message = None

    if form.validate_on_submit():
        uploaded_file = form.file.data 
        file_name = secure_filename(uploaded_file.filename) 
        secured_name = f"{uuid.uuid4().hex}_{file_name}" 
        job_role = form.job_role.data 
        job_descr = form.job_description.data 
        email = form.email.data
        company = form.company.data
        name = form.name.data
        try:

            # resume_file = io.BytesIO(uploaded_file.read()) 
            # print("resume file " , resume_file.)
            # s3_client.upload_fileobj(resume_file , Key = secured_name , Bucket = bucket_name)  
            uploaded_file.save(r'temp.pdf')
            # print("File Uploaded in S3")
            message = "Your File Was Uploaded Successfully"
            data = {
                "name" : name, 
                "company" : company, 
                "role" : job_role, 
                "description" : job_descr, 
                "email" : email
            }
            response = requests.post(url = URL  , json=data)
            if response.status_code == 200:
                print("File was Sent") 
            else:
                print(response.status_code)
                print("File wasn't sent" )
        except Exception as e:
            print("Couldn't Upload into S3 , error " , e)
            message = "Your File Was not uploaded, Try it again"
            
        
    return render_template("index.html", form = form , message = message) 

if __name__ == "__main__":
    app.run("0.0.0.0" , port = 5000) 
