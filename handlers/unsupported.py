from nlp_intern.root import app
from nlp_intern.logger import create_feedback_file

@app.handle(default=True)
@app.handle(intent='unknown')
def unknown(request, responder):
    create_feedback_file('unsupported',request)
    responder.reply('Not sure what you meant there...')
