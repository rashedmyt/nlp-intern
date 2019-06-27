from datetime import date
import os

def create_feedback_file(domain_name,request):
   today = date.today()
   cwd = os.getcwd()
   access_rights = 0o755
   foldername = cwd + '/nlp_intern/feedback'
   try:
       os.mkdir(foldername,access_rights)
       #print("fc")
   except OSError:
       print()

   domainfoldername = '/' + domain_name   
   try:
       os.mkdir(foldername+domainfoldername,access_rights)
       #print("ffc")
   except OSError:
       print()
    
   fname =  './nlp_intern/feedback/' + domain_name + "/" + today.strftime("%d%m%y")
   f = open(fname + ".txt",'a')
   f.write(request.text + '\n')
   f.close()


#create_feedback_file('greet','Hey ya')
