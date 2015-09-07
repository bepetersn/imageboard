
from flask import Flask, render_template, url_for, redirect, \
    send_from_directory, request
from forms import NewThreadForm, NewPostForm
from utils import ensure_dir, flash_form_errors
from models import Thread, Post, IPAddress, Poster, db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.jinja_env.filters['strftime'] = lambda t: t.strftime('%b %m %Y at %H:%I%p')
db.init_app(app)
ensure_dir('uploads')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           form=NewThreadForm(),
                           threads=Thread.query.join(Post)\
                                    .order_by(Post.time_created.desc()).all())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_DIR'],
                               filename)


@app.route('/new-thread/', methods=['POST'])
def new_thread():
    form = NewThreadForm()
    if form.validate_on_submit():
        data = form.data.copy()
        poster = Poster.get_or_create(
            ip_address=IPAddress.get_or_create(v4=request.remote_addr),
            name=data.pop('name')
        )
        t = poster.create_thread(**data)
        return redirect(url_for('thread', thread_id=t.id))
    else:
        flash_form_errors(form)
        return redirect(url_for('index'))


@app.route('/thread/<int:thread_id>/', methods=['GET'])
def thread(thread_id):
    return render_template('thread.html',
                           thread=Thread.query.get_or_404(thread_id),
                           form=NewPostForm())


@app.route('/thread/<int:thread_id>/new-post/', methods=['POST'])
def new_post(thread_id):
    t = Thread.query.get_or_404(thread_id)
    form = NewPostForm()
    if form.validate_on_submit():
        data = form.data.copy()
        poster = Poster.get_or_create(
            ip_address=IPAddress.get_or_create(v4=request.remote_addr),
            name=data.pop('name')
        )
        poster.create_post(t, **data)
    else:
        flash_form_errors(form)

    return redirect(url_for('thread', thread_id=thread_id))
