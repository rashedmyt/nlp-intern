from .root import app
from .root import qa


@app.handle(intent='last_recruitment')
def company_last_year(request, responder):
    company_name = None
    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']

    if company_name != None:
        companies = qa.get(index='companies', name=company_name)
        last_recruitment_year = sorted(companies[0]['data'].keys())[-1]

        responder.frame['company_name'] = company_name
        responder.frame['year'] = last_recruitment_year

        reply = company_name + " last came for placements in " + last_recruitment_year
        responder.reply(reply)
    else:
        responder.reply(
            "Sorry, couldn't find the company name in our database.")
