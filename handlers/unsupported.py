from nlp_intern.root import app
from . import filetest

@app.handle(default=True)
@app.handle(intent='unknown')
def unknown(request, responder):
    filetest.create_feedback_file('unsupported',request)
    responder.reply('Not sure what you meant there...')
