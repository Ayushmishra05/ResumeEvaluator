from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser 
from utils import load_config 
from config.CONFIG import OVERALL , selected_path
import json

class OverallAnalyser():
    def __init__(self):
        self.model = ChatGroq(model = 'llama-3.3-70b-versatile') 
        overall_config = load_config(OVERALL)
        self.template = ChatPromptTemplate([
            ("system" , overall_config['overall']), 
            ("human" , "Job Description ==> {job_description} , ATS_Keywords ==> {ats} , HR Insights ==> {hr} , Resume ==> {resume} , Job Role ==> {job}") 
        ])

        self.parser = StrOutputParser() 
    def analyse(self, text, descr, ats, hr , job):
        chain = self.template | self.model | self.parser
        output = chain.invoke({"resume" : text , "job_description" : descr, "ats" : ats, "hr" : hr , "job" : job})
        print(type(output) , output)
        score = json.loads(output)['Score']
        selected = {
            'Score' : score
        }
        with open(selected_path , 'w') as f:
            json.dump(selected , fp=f)
        return output