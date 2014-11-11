import os
from flask import Flask, render_template, request
from forms import assignRU
from wtforms import Form, TextField, PasswordField, IntegerField
from wtforms.validators import Required, Email, EqualTo, NumberRange
from Hanzo import *
from config import *

app = Flask(__name__)
app.config.from_object('config')
razor = RazorSession(RAZOR_REST_URL)



@app.route('/')
def index():
    nodeinfo = razor.getNodes()
    return render_template('index.html', nodeinfo = nodeinfo)

@app.route('/nodes')
def nodes():
    nodeinfo = razor.getNodes()
    return render_template('nodes.html', nodeinfo = nodeinfo)

@app.route('/assignru', methods=['GET', 'POST'])
def assignru():
    nodeinfo = razor.getNodes()
    fields = razor.getNodeNames(nodeinfo)
    for node in fields:
        setattr(assignRU, node, IntegerField('node RU', [NumberRange(min=1, max=60, message = 'Invalid Integer')]))
    form = assignRU(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('assignru.html', nodeinfo = nodeinfo, form=form, fields=form._fields)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
