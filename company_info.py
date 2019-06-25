from .root import app
from .root import qa


@app.handle(intent='last_recruitment')
def company_last_year(request, responder):
    company_name = request.frame.get('company_name')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']

    if company_name != None:
        company = qa.get(index='companies', name=company_name)[0]
        last_recruitment_year = sorted(company['data'].keys())[-1]

        responder.frame['company_name'] = company_name
        responder.frame['year'] = last_recruitment_year

        reply = company_name + " last came for placements in " + last_recruitment_year
        responder.reply(reply)
    else:
        responder.reply(
            "Sorry, couldn't find the company name in our database.")


@app.handle(intent='highest_salary')
def company_highest_salary(request, responder):
    company_name = request.frame.get('company_name')
    year = request.frame.get('year')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']
        elif i['type'] == 'sys_time':
            year = i['value'][0]['value'][0:4]

    if company_name != None:
        company = qa.get(index='companies', name=company_name)[0]

        responder.frame['company_name'] = company_name
        responder.frame['year'] = year

        if year != None:
            if year in company['data']:
                highest_salary = company['data'][year]['highest_sal']
                reply = company_name + " gave a highest salary of " + \
                    highest_salary + " in the year " + year
                responder.reply(reply)
            else:
                reply = company_name + " didn't came for placements in " + year
                responder.reply(reply)
    else:
        responder.reply(
            "Sorry, couldn't find the company name in our database.")
