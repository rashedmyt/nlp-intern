from nlp_intern.root import app, qa
from nlp_intern.logger import create_feedback_file
from .helpers import handle_companies_list, extract_year


@app.handle(intent='companies_list')
def list_companies(request, responder):
    create_feedback_file('placement_info', request)
    handle_companies_list("some", extract_year(request), responder)


@app.handle(intent='companies_all')
def list_all_companies(request, responder):
    create_feedback_file('placement_info', request)
    handle_companies_list("all", extract_year(request), responder)
