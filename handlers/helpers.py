from nlp_intern.root import app, qa
from nlp_intern.logger import create_feedback_file


@app.handle(intent='specify_entity')
def specify_entity(request, responder):
    create_feedback_file('helpers', request)
    year, company_name, dept_name = extract_entities(request)

    if company_name:
        try:
            if request.frame['desired_action'] == "last_recruitment":
                handle_last_recruitment(company_name, dept_name, responder)
            elif request.frame['desired_action'] == "salary":
                handle_salary(company_name, year, responder)
            elif request.frame['desired_action'] == 'total_recruits':
                if dept_name:
                    handle_total_recruits(
                        company_name, year, dept_name, responder)
                else:
                    handle_total_recruits(company_name, year, 'all', responder)

        except KeyError:
            responder.reply("Please specify some action")
    else:
        responder.reply(
            "Not sure which company you meant there. Can you please try again?")


# Extractors


def extract_entities(request):
    company_name = request.frame.get('company_name')
    dept_name = request.frame.get('dept_name')
    year = request.frame.get('year')

    for i in request.entities:
        if i['type'] == 'company_name':
            company_name = i['value'][0]['cname']
        elif i['type'] == 'dept_name':
            dept_name = i['value'][0]['cname']
        elif i['type'] == 'sys_time':
            year = i['value'][0]['value'][0:4]

    return year, company_name, dept_name


# Helpers


def handle_companies_list(category, year, responder):
    companies = qa.get(index='companies', size=100)
    if year == None:
        company_names = [i['name'] for i in companies]
    else:
        company_names = [i['name']
                         for i in companies if year in i['data']]

    if year != None and category == "some":
        responder.frame['year'] = year
    elif category == "all":
        responder.frame.pop('year', None)

    if len(company_names) == 0:
        reply = "Data unavailable"
    else:
        reply = "The companies which came for placements"
        if year != None:
            reply += " in " + year
        if category == "all" or len(company_names) < 6:
            reply += " are\n" + "\n".join(company_names)
        elif len(company_names) > 5:
            reply += " are\n" + "\n".join(company_names[:5])
            reply += "\nand %s more...." % (len(company_names)-5)
    responder.reply(reply)


def handle_last_recruitment(company_name, category, responder):
    company = qa.get(index='companies', name=company_name)[0]

    if category:
        last_recruitment_year = next(
            (i for i in company['data'] if category in company['data'][i]), None)
    else:
        last_recruitment_year = sorted(company['data'].keys())[-1]

    responder.frame['company_name'] = company_name
    responder.frame['year'] = last_recruitment_year
    responder.frame['dept_name'] = category

    reply = company_name
    if last_recruitment_year:
        reply += " last came for placements in " + last_recruitment_year
        if category:
            reply += " for " + category
    elif category:
        reply += " didn't came for placements for " + category

    responder.reply(reply)


def handle_salary(company_name, year, responder):
    company = qa.get(index='companies', name=company_name)[0]

    responder.frame['company_name'] = company_name
    if year:
        responder.frame['year'] = year

    if year in company['data']:
        try:
            salary = company['data'][year]['salary']
            reply = "%s gave a salary of %s lpa in the year %s" % (
                company_name, salary, year)
            responder.reply(reply)
        except KeyError:
            responder.reply("Data Not available")
    elif year:
        reply = company_name + " didn't came for placements in " + year
        responder.reply(reply)
    else:
        responder.frame['desired_action'] = 'salary'
        responder.reply("Of course, which year?")
        responder.listen()


def handle_total_recruits(company_name, year, category, responder):
    company = qa.get(index='companies', name=company_name)[0]

    responder.frame['company_name'] = company_name

    if category != "all":
        responder.frame['dept_name'] = category

    if year:
        responder.frame['year'] = year

    if year in company['data']:
        recruits = 0
        if category == 'all':
            for k in company['data'][year]:
                if k != 'salary':
                    recruits += company['data'][year][k]
        else:
            try:
                recruits = company['data'][year][category]
            except KeyError:
                reply = "%s didn't recruit for %s dept in %s" % (
                    company_name, category, year)
                responder.reply(reply)
                return
        reply = "%s recruited total of %s students " % (
                company_name, recruits)
        if category != 'all':
            reply += "from %s " % (category)
        reply += "in the year %s" % (year)
        responder.reply(reply)
    elif year:
        reply = company_name + " didn't came for placements in " + year
        responder.reply(reply)
    else:
        responder.frame['desired_action'] = 'total_recruits'
        responder.reply("Of course, which year?")
        responder.listen()
