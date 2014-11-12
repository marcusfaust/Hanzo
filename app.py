import os
from flask import Flask, render_template, request
from forms import assignRU, NodeIdentities
from wtforms import IntegerField
from wtforms.validators import NumberRange
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
        for node in fields:
            razor.updateRU(node,form.data[node])
        pass
    return render_template('assignru.html', nodeinfo = nodeinfo, form=form, fields=form._fields)


@app.route('/nodeidentities', methods=['GET', 'POST'])
def nodeidentities():
    nodeinfo = razor.getNodes()
    form = NodeIdentities(request.form)
    if request.method == 'POST' and form.validate():
        for i in range(0, form.count.data):
            octet = int(extractLastOctet(form.starting_ip.data)) + i
            hostid = int(form.first_hostname_id.data) + i
            slen = len(form.first_hostname_id.data)
            while(len(str(hostid)) < slen):
                hostid = '0' + str(hostid)
            hostname = form.hostname_prefix.data + hostid
            ip = (extractSubnet(form.starting_ip.data)) + str(octet)

        pass
    return render_template('nodeidentities.html', nodeinfo = nodeinfo, form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
