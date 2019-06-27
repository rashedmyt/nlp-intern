from nlp_intern.root import app
from nlp_intern.logger import create_feedback_file


@app.handle(intent='greet')
def welcome(request, responder):
    create_feedback_file('greeting', request)
    try:
        # Get user's name from session information in a request to personalize the greeting.
        responder.slots['name'] = request.context['name']
        prefix = "Hello {name}, "
    except KeyError:
        prefix = 'Hello, '

    welcome_msg = ("I am your placement info assistant. You can ask questions "
                   "related to campus placements.")

    responder.reply(prefix + welcome_msg)


@app.handle(intent='exit')
def default(request, responder):
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    # Respond with a random selection from one of the canned "goodbye" responses.
    responder.reply(['Bye!', 'Goodbye!', 'Have a nice day.', 'See you later.'])
