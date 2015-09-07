from flask import flash
import os

def ensure_dir(path):
    """
    Given a path, creates it if it
    does not already exist.

    """
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def flash_form_errors(form):
    """
    Given a form, uses Flask's flashing
    functionality to show users what errors
    their submission might have during their
    last request.

    """
    for errors in form.errors.iteritems():
        flash_errors(errors)


def flash_errors(errors, category='warning'):
    if isinstance(errors, tuple):
        flash("{0}: {1}".format(errors[0], errors[1][0]), category=category)