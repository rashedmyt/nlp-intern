from .root import app
from .root import qa
from .helpers import handle_highest_salary, handle_last_recruitment


@app.handle(intent='last_recruitment')
def company_last_year(request, responder):
    company_name = request.frame.get('company_name')

    company_name = next((e['value'][0]['cname']
                         for e in request.entities if e['type'] == 'company_name'), company_name)

    if company_name:
        handle_last_recruitment(company_name, responder)
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
        handle_highest_salary(company_name, year, responder)
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
