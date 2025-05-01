from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import json 
import ast  


class InsightsGeneration():
    def __init__(self):
        self.model = ChatGroq(model = 'llama-3.3-70b-versatile') 

        self.template = ChatPromptTemplate([
            ("system" , """you are a HR of a company MetricLabs where you are evaluataing candidates Resume, now you dont know about the 
             job post, but your only task is to get the insights from the resume, your task is to get the clear cut insights from the resume, in the resume, 
             whem i say that you are evaluating a resume, you need to check the consistencies across the resume, Internal consistency, External Consistency, and Structural consistency, 
             so you will be given the Text that is extracted from the resume, and you need to analyse the candidate, (Example : Whether a candidate is maintaining the relevant skills, and whether he is consistent across his work expereinces, projects, and skills),
             give me all the insights from the resume in bullet points, no extras, no addons, only clear insights from  the resume, in bullet points"""), 
            ("human" , "Resume ==> {resume_text}") 
        ])

        self.parser = StrOutputParser()
    
    def get_insights(self, text):
        chain = self.template | self.model | self.parser
        output = chain.invoke({"resume_text" : text})
        return output 

# if __name__ == "__main__":
#     ig = InsightsGeneration()
#     with open("temp.txt" , "r") as fp:
#         result = ig.get_insights(fp.read())
#     print(result)


