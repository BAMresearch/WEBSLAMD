from flask import render_template
from werkzeug.exceptions import NotFound


def handle_404(err):
    return render_template('404.html', message=err.message), 404


def handle_400(err):
    return render_template('400.html'), 400


class MaterialNotFoundException(NotFound):

    def __init__(self, message):
        self.message = message
        super(MaterialNotFoundException, self).__init__()
