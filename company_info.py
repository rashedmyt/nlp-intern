from .root import app
from .root import qa


@app.handle(intent='last_recruitment')
def company_last_year(request, responder):
    company_name = request.frame.get('company_name')

    company_name = next((e['value'][0]['cname']
                         for e in request.entities if e['type'] == 'company_name'), company_name)

    if company_name:
        _handle_last_recruitment(company_name, responder)
    else:
        responder.frame['desired_action'] = "last_recruitment"
        responder.reply(
            "Sure, which company's last recruitment would you like to know?")
        responder.listen()


@app.handle(intent='highest_salary')
def company_highest_salary(request, responder):
    company_name = request.frame.get('company_name')
    year = request.frame.get('year')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']
        elif i['type'] == 'sys_time':
            year = i['value'][0]['value'][0:4]

    if company_name and year:
        _handle_highest_salary(company_name, year, responder)
    elif company_name:
        responder.frame['company_name'] = company_name
        responder.frame['desired_action'] = "highest_salary"

        responder.reply("Which year's highest salary would you like to know?")
        responder.listen()
    else:
        responder.frame['year'] = year
        responder.frame['desired_action'] = "highest_salary"

        responder.reply(
            "Sure, which company's highest salary would you like to know?")
        responder.listen()


@app.handle(intent='specify_company')
def specify_company(request, responder):
    year = request.frame.get('year')
    company_name = next((e['value'][0]['cname']
                         for e in request.entities if e['type'] == 'company_name'), None)

    if company_name:
        try:
            if request.frame['desired_action'] == "last_recruitment":
                _handle_last_recruitment(company_name, responder)
            elif request.frame['desired_action'] == "highest_salary":
                _handle_highest_salary(company_name, year, responder)
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
                _handle_highest_salary(company_name, year, responder)
        except KeyError:
            print("Please specify some action")
    else:
        responder.reply(
            "Not sure which company you meant there. Can you please try again?")


# Helpers


def _handle_last_recruitment(company_name, responder):
    company = qa.get(index='companies', name=company_name)[0]
    last_recruitment_year = sorted(company['data'].keys())[-1]

    responder.frame['company_name'] = company_name
    responder.frame['year'] = last_recruitment_year

    reply = company_name + " last came for placements in " + last_recruitment_year
    responder.reply(reply)


def _handle_highest_salary(company_name, year, responder):
    company = qa.get(index='companies', name=company_name)[0]

    responder.frame['company_name'] = company_name

    if year in company['data']:
        responder.frame['year'] = year
        highest_salary = company['data'][year]['highest_sal']
        reply = company_name + " gave a highest salary of " + \
            highest_salary + " in the year " + year
        responder.reply(reply)
    elif year:
        responder.frame['year'] = year
        reply = company_name + " didn't came for placements in " + year
        responder.reply(reply)
    else:
        responder.frame['desired_action'] = "highest_salary"
        responder.reply("Of course, which year?")
        responder.listen()
