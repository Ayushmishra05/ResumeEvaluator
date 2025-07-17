from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from utils import load_config 
from config.CONFIG import ATSCONFIG
import json 
import ast 

class GetKeywords():
    def __init__(self):
        self.model = ChatGroq(model = 'llama-3.3-70b-versatile') 
        ats_config = load_config(ATSCONFIG)
        self.template = ChatPromptTemplate([
            ("system" , ats_config['ats']), 
            ("human" , "Resume ==> {resume_text}") 
        ])

        self.parser = JsonOutputParser()
    def invoker(self, text):
        print("Inside Invoker")
        chain = self.template | self.model | self.parser
        output = chain.invoke({"resume_text" : text})
        return output

# if __name__ == "__main__":
#     kw = GetKeywords() 
#     with open("temp.txt" , "r") as fp:
#         result = kw.invoker(fp.read())
#     print(result)

