from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser 

class OverallAnalyser():
    def __init__(self):
        self.model = ChatGroq(model = 'llama-3.3-70b-versatile') 

        self.template = ChatPromptTemplate([
            ("system" , """You are a Manager Of MetricLabs Software Ltd, Now you get the Resume, and also the ATS Keywords, and Insights from the HR 
             about the resume, now you are the main person in the company, who will decide whether the particular candidate is selected for the interview or not 
             Now with great power comes great responsibility, now you need to go through the keywords, HR Insights, and the Rsume Itself to evaluate candidates Performance for the Job role, which the company has posted
             you will be given with the Job Description also, now you need to output in the Dictionary format, including Selected : <yes/no> , Reason : "<your Reason>" , no extras, no additional statements, no addons, only dictionary output"""), 
            ("human" , "Job Description ==> {job_description} , ATS_Keywords ==> {ats} , HR Insights ==> {hr} , Resume ==> {resume}") 
        ])

        self.parser = StrOutputParser() 
    def analyse(self, text, descr, ats, hr):
        chain = self.template | self.model | self.parser
        output = chain.invoke({"resume" : text , "job_description" : descr, "ats" : ats, "hr" : hr })
        output = output.replace("```json" , "")
        output = output.replace("```" , "") 
        return output