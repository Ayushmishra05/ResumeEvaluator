from PyPDF2 import PdfReader 
import urllib.request 
from ats import GetKeywords
from insights_generation import InsightsGeneration 
from overall_analyser import OverallAnalyser 
import ast

class ResumeToText():
    def __init__(self , url , descr):
        self.path = "temp.pdf"
        self.url = url 
        self.descr = descr
        

    def download_pdf(self):
        urllib.request.urlretrieve(self.url, self.path)

    
    def convert_to_text(self):
        self.download_pdf()
        reader = PdfReader(self.path) 
        with open("temp.txt" , "w" , encoding = "utf-8") as fp:
            for page in reader.pages:
                text = page.extract_text() 
                if text:
                    fp.write(text + "\n")
    def get_text(self):
        with open("temp.txt" , "r") as fp:
            result = fp.read() 
        return result 
    
    def get_ats(self, text ):
        ats = GetKeywords() 
        out_dict = ats.invoker(text) 
        return out_dict 
    
    def get_ins(self, text ):
        insights_gen = InsightsGeneration() 
        insights = insights_gen.get_insights(text) 
        return insights 
    
    def analyse_overall(self):
        self.convert_to_text()
        text = self.get_text()
        oa = OverallAnalyser()
        kw = self.get_ats(text)
        ins = self.get_ins(text) 
        analysis = oa.analyse(text, self.descr, kw, ins)  

        return ast.literal_eval(analysis) 
      
          
        

# if __name__ == "__main__":
#     rtt = ResumeToText("https://resumesbyevaluator.s3.us-east-1.amazonaws.com/14eb2df699be4a56956e6c4ec3f5064c_evaluation_report_11.pdf")
#     print(rtt.analyse_overall())