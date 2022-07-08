from flask import render_template
from werkzeug.exceptions import NotFound, BadRequest


def handle_404(err):
    return render_template('404.html', message=err.message), 404


def handle_400(err):
    return render_template('400.html', message=err.message), 400


class MaterialNotFoundException(NotFound):

    def __init__(self, message):
        self.message = message
        super(MaterialNotFoundException, self).__init__()


class ValueNotSupportedException(BadRequest):

    def __init__(self, message):
        self.message = message
        super(ValueNotSupportedException, self).__init__()
