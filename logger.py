from datetime import date
import logging
import os


feedback_dir = 'nlp_intern/feedback/'


def create_feedback_file(domain_name, request):
    log_dir = feedback_dir + domain_name
    os.makedirs(log_dir, exist_ok=True)
    log_file = "%s/%s.txt" % (log_dir, str(date.today()))

    # remove any handlers present in root
    # so that basicConfig can execute
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # setup logging and log the text
    logging.basicConfig(filename=log_file,
                        level=logging.INFO, format='%(message)s')
    logging.info(request.text)
