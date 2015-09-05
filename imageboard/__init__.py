
from flask import Flask, render_template, url_for, redirect

from forms import NewThreadForm
from models import Thread


app = Flask(__name__)
app.debug = True
app.secret_key = 'fake'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', form=NewThreadForm())


@app.route('/new-thread/', methods=['POST'])
def new_thread():
    f = NewThreadForm()
    if f.validate_on_submit():
        t = Thread.from_details(**f.data)
        return redirect(url_for('thread', id=t.id))
    else:
        # deal with bad forms later
        pass


@app.route('/thread/<int:id>/')
def thread(id):
    t = Thread.query.get(id)
    if t is None:
        return 'No such thread.', 500
    else:
        return ('Thread #{}: '
                'Created on {} '
                'Subject: {} '
                'Poster: {} '
                'Comment: {}'.format(
                    t.id,
                    t.details.time_created.strftime('%b %m %Y at %H:%I%p'),
                    t.subject,
                    t.details.name,
                    t.details.comment
                ), 200)


if __name__ == '__main__':
    app.run()