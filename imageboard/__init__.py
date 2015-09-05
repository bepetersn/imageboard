
from flask import Flask, render_template, url_for, redirect

from forms import NewThreadForm
from models import Thread


app = Flask(__name__)
app.debug = True
app.secret_key = 'fake'
app.jinja_env.filters['strftime'] = lambda t: t.strftime('%b %m %Y at %H:%I%p')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', form=NewThreadForm())


@app.route('/new-thread/', methods=['POST'])
def new_thread():
    form = NewThreadForm()
    if form.validate_on_submit():
        t = Thread.from_details(**form.data)
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
        return render_template('thread.html', t=t)


if __name__ == '__main__':
    app.run()