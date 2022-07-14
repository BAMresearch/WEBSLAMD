from flask import render_template
from werkzeug.exceptions import NotFound, BadRequest, RequestEntityTooLarge


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


class MaterialNotFoundException(NotFound):

    def __init__(self, message):
        self.message = message
        super(MaterialNotFoundException, self).__init__()


class ValueNotSupportedException(BadRequest):

    def __init__(self, message):
        self.message = message
        super(ValueNotSupportedException, self).__init__()


class SlamdRequestTooLargeException(RequestEntityTooLarge):
    def __init__(self, message):
        self.message = message
        super(SlamdRequestTooLargeException, self).__init__()
