from datetime import date
import os

def create_feedback_file(intentname,request):
   today = date.today()
   cwd = os.getcwd()
   files = os.listdir(cwd)
   print(files)
   fname =  './nlp_intern/handlers/feedback/' + intentname + "/" + today.strftime("%d%m%y")
   f = open(fname + ".txt",'a')
   f.write(request.text + '\n')



#create_feedback_file('greet','Hey ya')
