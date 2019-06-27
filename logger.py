from datetime import date
import os

def create_feedback_file(domain_name,request):
   today = date.today()
   cwd = os.getcwd()
   fname =  './nlp_intern/feedback/' + domain_name + "/" + today.strftime("%d%m%y")
   f = open(fname + ".txt",'a')
   f.write(request.text + '\n')



#create_feedback_file('greet','Hey ya')
