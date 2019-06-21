from .root import app
from .root import qa


@app.handle(intent='companies_list')
def list_companies(request, responder):
    companies = qa.get(index='companies')
    company_names = '\n'.join(c['name'] for c in companies)
    responder.reply(
        "The following companies came for placements\n" + company_names)
