from PyPDF2 import PdfReader 
import urllib.request 
from resume_process.ats import GetKeywords
from resume_process.insights_generation import InsightsGeneration 
from resume_process.overall_analyser import OverallAnalyser 
import ast

class ResumeToText():
    def __init__(self  , job , descr):
        self.path = "temp.pdf"
        self.descr = descr
        self.text = "temp.txt"
        self.job = job
        
    
    def convert_to_text(self):
        reader = PdfReader(self.path) 
        with open(self.text , "w" , encoding = "utf-8") as fp:
            for page in reader.pages:
                text = page.extract_text() 
                if text:
                    fp.write(text + "\n")

    def get_text(self):
        with open(self.text , "r" , encoding="utf-8") as fp:
            result = fp.read() 
        return result 
    
    def get_ats(self, text ):
        ats = GetKeywords() 
        out_dict = ats.invoker(text) 
        return out_dict 
    
    def get_ins(self, text ):
        insights_gen = InsightsGeneration() 
        insights, html = insights_gen.get_insights(text , self.descr , self.job) 
        return insights , html 
    
    def analyse_overall(self):
        self.convert_to_text()
        text = self.get_text()
        oa = OverallAnalyser()
        kw = self.get_ats(text)
        ins , html = self.get_ins(text) 
        analysis = oa.analyse(text, self.descr, kw, ins , self.job)  

        return ast.literal_eval(analysis) , html
      
          
        

# if __name__ == "__main__":
#     rtt = ResumeToText("https://resumesbyevaluator.s3.us-east-1.amazonaws.com/14eb2df699be4a56956e6c4ec3f5064c_evaluation_report_11.pdf")
#     print(rtt.analyse_overall())