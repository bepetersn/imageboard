
from flask import Flask, render_template, url_for, redirect, send_from_directory
from forms import NewThreadForm, NewPostForm
from utils import ensure_dir, flash_form_errors
from models import Thread, Post, db


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.jinja_env.filters['strftime'] = lambda t: t.strftime('%b %m %Y at %H:%I%p')
db.init_app(app)
ensure_dir('uploads')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           form=NewThreadForm(),
                           threads=Thread.query.join(Post).order_by(Post.time_created.desc()).all())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_DIR'],
                               filename)


@app.route('/new-thread/', methods=['POST'])
def new_thread():
    form = NewThreadForm()
    if form.validate_on_submit():
        thread = Thread.from_details(**form.data)
        return redirect(url_for('thread', id=thread.id))
    else:
        flash_form_errors(form)
        return redirect(url_for('index'))


@app.route('/thread/<int:id>/', methods=['GET'])
def thread(id):
    return render_template('thread.html',
                           thread=Thread.query.get_or_404(id),
                           form=NewPostForm())


@app.route('/thread/<int:thread_id>/new-post/', methods=['POST'])
def new_post(id):
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(thread=Thread.query.get_or_404(id),
                    **form.data)
        post.save()
    else:
        flash_form_errors(form)

    return redirect(url_for('thread', id=id))