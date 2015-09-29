from functools import wraps
from flask import Flask, render_template, url_for, redirect, \
    send_from_directory, flash
from werkzeug.utils import secure_filename
from forms import NewThreadForm, NewPostForm
from utils import ensure_dir, flash_form_errors
from models import Thread, Post, IPAddress, Poster, db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.jinja_env.filters['strftime'] = lambda t: t.strftime('%b %m %Y at %H:%I%p')
db.init_app(app)
ensure_dir('uploads')


def filter_on_ips(f):
    """
    Decorator for denying access to routes based on a 'blocked'
    flag set on the ip_addresses table of our database.

    """
    @wraps(f)
    def _filter(*args, **kwargs):
        ip_address = IPAddress.from_request()
        if ip_address.blocked:
            flash('You have been blocked from posting. Contact support '
                  'for more information.')
            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return _filter


@app.route('/', methods=['GET'])
def index():
    """
    Index, showing a "NewThreadForm" and a
    list of all existing threads.

    """
    return render_template('index.html',
                           form=NewThreadForm(),
                           threads=Thread.query.join(Post)\
                                    .order_by(Post.time_created.desc()).all())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serves the files in the 'uploads' folder.
    """
    return send_from_directory(app.config['UPLOADS_DIR'],
                               secure_filename(filename))


@app.route('/new-thread/', methods=['POST'])
@filter_on_ips
def new_thread():
    """
    POST API endpoint for creating new threads.
    """

    form = NewThreadForm()
    if form.validate_on_submit():

        data = form.data.copy()
        poster = Poster.from_details(data.pop('name'))
        t = poster.create_thread(**data)
        return redirect(url_for('thread', thread_id=t.id))

    else:
        flash_form_errors(form)
        return redirect(url_for('index'))


@app.route('/thread/<int:thread_id>/', methods=['GET'])
def thread(thread_id):
    """
    Detail page for threads, which returns a 404 if
    the thread with the given `thread_id` does not exist.

    """
    return render_template('thread.html',
                           thread=Thread.query.get_or_404(thread_id),
                           form=NewPostForm())


@app.route('/thread/<int:thread_id>/new-post/', methods=['POST'])
@filter_on_ips
def new_post(thread_id):
    """
    POST API endpoint for creating a new post for the thread
    with given `thread_id`. Also returns a 404 if it doesn't exist.

    """

    t = Thread.query.get_or_404(thread_id)
    form = NewPostForm()
    if form.validate_on_submit():

        data = form.data.copy()
        poster = Poster.from_details(data.pop('name'))
        poster.create_post(t, **data)
        return redirect(url_for('thread', thread_id=thread_id))

    else:
        flash_form_errors(form)

    return redirect(url_for('thread', thread_id=thread_id))
