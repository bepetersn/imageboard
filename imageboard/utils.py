from flask import flash
import os

def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def flash_form_errors(form):
    for errors in form.errors.iteritems():
        flash_errors(errors)


def flash_errors(errors, category='warning'):
    if isinstance(errors, tuple):
        flash("{0}: {1}".format(errors[0], errors[1][0]), category=category)