
import os
from flask import Flask, render_template, url_for, redirect, send_from_directory
from forms import NewThreadForm, NewPostForm
from models import Thread, Post


app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.jinja_env.filters['strftime'] = lambda t: t.strftime('%b %m %Y at %H:%I%p')


def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


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
        # deal with bad forms later
        pass

@app.route('/thread/<int:id>/', methods=['GET'])
def thread(id):
    thread = Thread.query.get(id)
    if thread is None:
        return 'No such thread.', 404
    else:
        return render_template('thread.html',
                               thread=thread,
                               form=NewPostForm())


@app.route('/thread/<int:thread_id>/new-post/', methods=['POST'])
def new_post(thread_id):
    thread = Thread.query.get(thread_id)
    if thread is None:
        return 'No such thread.', 500
    else:
        form = NewPostForm()
        if form.validate_on_submit():
            post = Post(thread=thread, **form.data)
            post.save()
            return redirect(url_for('thread', id=thread.id))
        else:
            # deal with bad forms later
            pass


if __name__ == '__main__':
    app.run()