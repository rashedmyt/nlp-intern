from nlp_intern.root import app, qa
from nlp_intern.logger import create_feedback_file
from .helpers import handle_companies_list, extract_entities
import math


@app.handle(intent='companies_list')
def list_companies(request, responder):
    create_feedback_file('placement_info', request)
    year, *_ = extract_entities(request)
    handle_companies_list("some", year, responder)


@app.handle(intent='companies_all')
def list_all_companies(request, responder):
    create_feedback_file('placement_info', request)
    year, *_ = extract_entities(request)
    handle_companies_list("all", year, responder)


@app.handle(intent='company_count')
def count_companies(request, responder):
    create_feedback_file('placement_info', request)
    year, *_ = extract_entities(request)

    responder.frame.pop('year', None)

    companies = qa.get(index='companies', size=100)
    count = 0

    for i in companies:
        if year in i['data']:
            count += 1

    reply = "A total of "
    if year != None:
        reply += "%s companies visited in %s." % (count, year)
    else:
        reply += "%s companies have visited till now." % (len(companies))

    responder.reply(reply)


@app.handle(intent='companies_higher_salary')
def higher_salary_companies(request, responder):
    create_feedback_file('placement_info', request)
    year, *_ = extract_entities(request)

    salary = next((i['value'][0]['value']
                   for i in request.entities if i['type'] == 'sys_number'), None)

    responder.frame.pop('year', None)

    companies = qa.get(index='companies', size=100)
    count = 0

    if year:
        for i in companies:
            if year in i['data']:
                if salary < i['data'][year]['salary']:
                    count += 1
    else:
        for i in companies:
            for k in i['data']:
                if salary < i['data'][k]['salary']:
                    count += 1
                    break

    reply = "A total of %s " % (count)
    if count == 1:
        reply += "company"
    else:
        reply += "companies"
    reply += " gave a salary higher than %s lpa" % (salary)
    if year:
        reply += " in the year %s" % (year)
    responder.reply(reply)


@app.handle(intent='companies_lower_salary')
def lower_salary_companies(request, responder):
    create_feedback_file('placement_info', request)
    year, *_ = extract_entities(request)

    salary = next((i['value'][0]['value']
                   for i in request.entities if i['type'] == 'sys_number'), None)

    responder.frame.pop('year', None)

    companies = qa.get(index='companies', size=100)
    count = 0

    if year:
        for i in companies:
            if year in i['data']:
                if salary > i['data'][year]['salary']:
                    count += 1
    else:
        for i in companies:
            for k in i['data']:
                if salary > i['data'][k]['salary']:
                    count += 1
                    break

    reply = "A total of %s " % (count)
    if count == 1:
        reply += "company"
    else:
        reply += "companies"
    reply += " gave a salary lower than %s lpa" % (salary)
    if year:
        reply += " in the year %s" % (year)
    responder.reply(reply)


@app.handle(intent='companies_salary')
def salary_companies(request, responder):
    create_feedback_file('placement_info', request)
    year, *_ = extract_entities(request)

    salary = next((i['value'][0]['value']
                   for i in request.entities if i['type'] == 'sys_number'), None)

    responder.frame.pop('year', None)

    companies = qa.get(index='companies', size=100)
    count = 0

    if year:
        for i in companies:
            if year in i['data']:
                if salary == math.floor(i['data'][year]['salary']):
                    count += 1
    else:
        for i in companies:
            for k in i['data']:
                if salary == math.floor(i['data'][k]['salary']):
                    count += 1
                    break

    reply = "A total of %s " % (count)
    if count == 1:
        reply += "company"
    else:
        reply += "companies"
    reply += " gave a salary of %s lpa" % (salary)
    if year:
        reply += " in the year %s" % (year)
    responder.reply(reply)
