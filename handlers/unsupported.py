from nlp_intern.root import app


@app.handle(default=True)
@app.handle(intent='unknown')
def unknown(request, responder):
    responder.reply('Not sure what you meant there...')
