from nlp_intern.root import app
from nlp_intern.root import qa
from . import filetest as ft

@app.handle(intent='companies_list')
def list_companies(request, responder):
    ft.create_feedback_file('placement_info',request)
    asked_year = None

    for i in request.entities:
        if i['type'] == 'sys_time':
            asked_year = i['value'][0]['value'][0:4]
            break
    companies = qa.get(index='companies')
    if asked_year == None:
        company_names = [i['name'] for i in companies]
    else:
        responder.frame['year'] = asked_year
        company_names = [i['name']
                         for i in companies if asked_year in i['data']]

    if len(company_names) == 0:
        reply = "No companies came for placements"
        if asked_year != None:
            reply += " in " + asked_year
    else:
        reply = "The companies which came for placements"
        if asked_year != None:
            reply += " in " + asked_year
        reply += " are\n" + "\n".join(company_names)

    responder.reply(reply)
