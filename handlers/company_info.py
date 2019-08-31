from nlp_intern.root import app, qa
from .helpers import handle_salary, handle_last_recruitment, handle_total_recruits, extract_entities
from nlp_intern.logger import create_feedback_file


@app.handle(intent='last_recruitment')
def company_last_year(request, responder):
    create_feedback_file('company_info', request)
    _, company_name, _ = extract_entities(request)

    responder.frame['desired_action'] = "last_recruitment"

    if company_name:
        handle_last_recruitment(company_name, responder)
    else:
        responder.reply(
            "Sure, which company's last recruitment would you like to know?")
        responder.listen()


@app.handle(intent='salary')
def company_salary(request, responder):
    create_feedback_file('company_info', request)
    year, company_name, _ = extract_entities(request)

    responder.frame['desired_action'] = 'salary'

    if company_name and year:
        handle_salary(company_name, year, responder)
    elif company_name:
        responder.frame['company_name'] = company_name

        responder.reply("Which year's salary would you like to know?")
        responder.listen()
    else:
        responder.frame['year'] = year

        responder.reply(
            "Sure, which company's salary would you like to know?")
        responder.listen()


@app.handle(intent='total_recruits')
def company_total_recruits(request, responder):
    create_feedback_file('company_info', request)
    year, company_name, dept_name = extract_entities(request)

    responder.frame['desired_action'] = 'total_recruits'

    if dept_name:
        category = dept_name
    else:
        category = 'all'

    if company_name and year:
        handle_total_recruits(company_name, year, category, responder)
    elif company_name:
        responder.frame['company_name'] = company_name

        responder.reply("Which year's total recruits would you like to know?")
        responder.listen()
    else:
        responder.frame['year'] = year

        responder.reply(
            "Sure, which company's total recruits would you like to know?")
        responder.listen()
