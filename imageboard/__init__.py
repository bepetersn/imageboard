
from flask import Flask, render_template, url_for, redirect
from forms import NewThreadForm
#from models import Thread


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
        # deal with creating real threads
        return redirect(url_for('thread', id=0))
    else:
        # deal with later
        pass


@app.route('/thread/<int:id>/')
def thread(id):
    # show the thread here
    return 'Thread #{}'.format(id), 200


if __name__ == '__main__':
    app.run()