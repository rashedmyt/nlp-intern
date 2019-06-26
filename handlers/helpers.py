from nlp_intern.root import app
from nlp_intern.root import qa


@app.handle(intent='specify_company')
def specify_company(request, responder):
    year = request.frame.get('year')
    company_name = next((e['value'][0]['cname']
                         for e in request.entities if e['type'] == 'company_name'), None)

    if company_name:
        try:
            if request.frame['desired_action'] == "last_recruitment":
                handle_last_recruitment(company_name, responder)
            elif request.frame['desired_action'] == "highest_salary":
                handle_salary(company_name, year, "highest", responder)
            elif request.frame['desired_action'] == "lowest_salary":
                handle_salary(company_name, year, "lowest", responder)
        except KeyError:
            print("please specify some action")
    else:
        responder.reply(
            "Not sure which company you meant there. Can you please try again?")


@app.handle(intent='specify_year')
def specify_year(request, responder):
    company_name = request.frame.get('company_name')
    year = next((e['value'][0]['value'][0:4]
                 for e in request.entities if e['type'] == 'sys_time'), None)
    print(year)
    if company_name:
        try:
            if request.frame['desired_action'] == "highest_salary":
                handle_salary(company_name, year, "highest", responder)
            elif request.frame['desired_action'] == "lowest_salary":
                handle_salary(company_name, year, "lowest", responder)
        except KeyError:
            print("Please specify some action")
    else:
        responder.reply(
            "Not sure which company you meant there. Can you please try again?")


# Helpers


def handle_last_recruitment(company_name, responder):
    company = qa.get(index='companies', name=company_name)[0]
    last_recruitment_year = sorted(company['data'].keys())[-1]

    responder.frame['company_name'] = company_name
    responder.frame['year'] = last_recruitment_year

    reply = company_name + " last came for placements in " + last_recruitment_year
    responder.reply(reply)


def handle_salary(company_name, year, category, responder):
    company = qa.get(index='companies', name=company_name)[0]

    responder.frame['company_name'] = company_name

    if year in company['data']:
        responder.frame['year'] = year
        salary = company['data'][year]['%s_sal' % (category)]
        reply = "%s gave a %s salary of %s in the year %s" % (
            company_name, category, salary, year)
        responder.reply(reply)
    elif year:
        responder.frame['year'] = year
        reply = company_name + " didn't came for placements in " + year
        responder.reply(reply)
    else:
        responder.frame['desired_action'] = "%s_salary" % (category)
        responder.reply("Of course, which year?")
        responder.listen()
