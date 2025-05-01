from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import json 
import ast 

class GetKeywords():
    def __init__(self):
        self.model = ChatGroq(model = 'llama-3.3-70b-versatile') 

        self.template = ChatPromptTemplate([
            ("system" , """you are a ATS, your task is to check the resume text, and get the Relevant Keywords from the Resume, 
             You will be given with the Text that has been extracted from the Resume, you will get the relevant keywords, 
             ignore other details like Addressm and all 
            You can Extract informations like Skills, Experience, Contributions, Work Experience, Education Details, Achievement, 
             University Scores, and other relevant Information, Make sure to get the Keywords only nad not full text, 
             give the output in the JSON format no extras, nothing much extra, 
             i want the output in json format only, something like this inside the json,  Keywords : ["<keyword1>" , "<keyword2"> , ... "<keyword_n>"] """), 
            ("human" , "Resume ==> {resume_text}") 
        ])

        self.parser = StrOutputParser()
    def invoker(self, text):
        print("Inside Invoker")
        chain = self.template | self.model | self.parser
        output = chain.invoke({"resume_text" : text})
        return ast.literal_eval(output)

# if __name__ == "__main__":
#     kw = GetKeywords() 
#     with open("temp.txt" , "r") as fp:
#         result = kw.invoker(fp.read())
#     print(result)

