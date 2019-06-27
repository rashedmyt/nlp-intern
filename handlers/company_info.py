from nlp_intern.root import app, qa
from .helpers import handle_salary, handle_last_recruitment
from nlp_intern.logger import create_feedback_file


@app.handle(intent='last_recruitment')
def company_last_year(request, responder):
    create_feedback_file('company_info', request)
    company_name = request.frame.get('company_name')

    company_name = next((e['value'][0]['cname']
                         for e in request.entities if e['type'] == 'company_name'), company_name)

    responder.frame['desired_action'] = "last_recruitment"

    if company_name:
        handle_last_recruitment(company_name, responder)
    else:
        responder.reply(
            "Sure, which company's last recruitment would you like to know?")
        responder.listen()


@app.handle(intent='highest_salary')
def company_highest_salary(request, responder):
    create_feedback_file('company_info', request)
    company_name = request.frame.get('company_name')
    year = request.frame.get('year')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']
        elif i['type'] == 'sys_time':
            year = i['value'][0]['value'][0:4]

    responder.frame['desired_action'] = "highest_salary"

    if company_name and year:
        handle_salary(company_name, year, "highest", responder)
    elif company_name:
        responder.frame['company_name'] = company_name

        responder.reply("Which year's highest salary would you like to know?")
        responder.listen()
    else:
        responder.frame['year'] = year

        responder.reply(
            "Sure, which company's highest salary would you like to know?")
        responder.listen()


@app.handle(intent='lowest_salary')
def company_lowest_salary(request, responder):
    create_feedback_file('company_info', request)
    company_name = request.frame.get('company_name')
    year = request.frame.get('year')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']
        elif i['type'] == 'sys_time':
            year = i['value'][0]['value'][0:4]

    responder.frame['desired_action'] = "lowest_salary"

    if company_name and year:
        handle_salary(company_name, year, "lowest", responder)
    elif company_name:
        responder.frame['company_name'] = company_name

        responder.reply("Which year's lowest salary would you like to know?")
        responder.listen()
    else:
        responder.frame['year'] = year

        responder.reply(
            "Sure, which company's lowest salary would you like to know?")
        responder.listen()


@app.handle(intent='average_salary')
def company_average_salary(request, responder):
    create_feedback_file('company_name', request)
    company_name = request.frame.get('company_name')
    year = request.frame.get('year')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']
        elif i['type'] == 'sys_time':
            year = i['value'][0]['value'][0:4]

    responder.frame['desired_action'] = "average_salary"

    if company_name and year:
        handle_salary(company_name, year, "average", responder)
    elif company_name:
        responder.frame['company_name'] = company_name

        responder.reply("Which year's average salary would you like to know?")
        responder.listen()
    else:
        responder.frame['year'] = year

        responder.reply(
            "Sure, which company's average salary would you like to know?")
        responder.listen()
