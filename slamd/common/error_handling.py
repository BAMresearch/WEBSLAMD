from flask import render_template
from werkzeug.exceptions import NotFound, BadRequest, RequestEntityTooLarge, UnprocessableEntity, Forbidden, \
    RequestTimeout


def handle_404(err):
    try:
        return render_template('404.html', message=err.message), 404
    except AttributeError:
        return render_template('404.html', message='The requested page is not available.'), 404


def handle_400(err):
    try:
        return render_template('400.html', message=err.message), 400
    except AttributeError:
        return render_template('400.html', message='You are not allowed to access the requested resource.'), 400


def handle_413(err):
    try:
        return render_template('413.html', message=err.message), 413
    except AttributeError:
        return render_template('413.html', message='Request is too large.'), 413


def handle_422(err):
    try:
        return render_template('422.html', message=err.message), 422
    except AttributeError:
        return render_template('422.html', message='Cannot process provided entity or data.'), 422


def handle_403(err):
    try:
        return render_template('403.html', message=err.message), 403
    except AttributeError:
        return render_template('403.html', message='Free tier exhausted. Please provide your token.'), 403


def handle_408(err):
    try:
        return render_template('408.html', message=err.message), 408
    except AttributeError:
        return render_template('408.html', message='LLM not available.'), 408


class MaterialNotFoundException(NotFound):

    def __init__(self, message):
        super().__init__()
        self.message = message


class PlotDataNotFoundException(NotFound):

    def __init__(self, message):
        super().__init__()
        self.message = message


class DatasetNotFoundException(NotFound):

    def __init__(self, message):
        super().__init__()
        self.message = message


class ValueNotSupportedException(BadRequest):

    def __init__(self, message):
        super().__init__()
        self.message = message


class SlamdRequestTooLargeException(RequestEntityTooLarge):
    def __init__(self, message):
        super().__init__()
        self.message = message


class SequentialLearningException(UnprocessableEntity):
    def __init__(self, message):
        super().__init__()
        self.message = message


class SlamdUnprocessableEntityException(UnprocessableEntity):
    def __init__(self, message):
        super().__init__()
        self.message = message


class FreeTrialLimitExhaustedException(Forbidden):
    def __init__(self, message):
        super().__init__()
        self.message = message


class LLMNotRespondingException(RequestTimeout):
    def __init__(self, message):
        super().__init__()
        self.message = message
