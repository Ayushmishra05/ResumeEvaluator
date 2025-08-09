from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from config.CONFIG import INSIGHT
from utils import load_config
import json 
import ast  
import yaml 

class InsightsGeneration():
    def __init__(self):
        self.model = ChatGroq(model = 'llama-3.3-70b-versatile') 
        insight_config = load_config(INSIGHT)
        self.template = ChatPromptTemplate([
            ("system" , insight_config['insight']), 
            ("human" , "Resume ==> {resume_text} , job_role ==> {job} , job_description ==> {descr}") 
        ])

        self.parser = JsonOutputParser()
    def get_insights(self, text , descr , job):
        chain = self.template | self.model | self.parser
        output = chain.invoke({"resume_text" : text , "descr" : descr, "job" : job})
        print("Insight " , output)
        return output['plain_text'] , output['html'] 

# if __name__ == "__main__":
#     ig = InsightsGeneration()
#     with open("temp.txt" , "r") as fp:
#         result = ig.get_insights(fp.read())
#     print(result)


