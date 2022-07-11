from flask import render_template


def handle_404(err):
    return render_template('404.html'), 404


def handle_400(err):
    return render_template('400.html'), 400
