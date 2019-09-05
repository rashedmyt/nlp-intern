from nlp_intern.root import app, qa
from nlp_intern.logger import create_feedback_file
from .helpers import handle_companies_list, extract_entities


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
