import os
from flask import Flask, render_template, request, redirect, url_for
from forms import assignRU, NodeIdentities, ESXiGlobalParams
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
    esxi_subnetmask = razor.esxi_subnetmask
    esxi_default_gw = razor.esxi_default_gw
    esxi_dns = razor.esxi_dns
    esxi_domain_suffix = razor.esxi_domain_suffix
    return render_template('index.html', nodeinfo = nodeinfo, esxi_subnetmask = esxi_subnetmask, esxi_default_gw = esxi_default_gw, esxi_dns = esxi_dns, esxi_domain_suffix = esxi_domain_suffix)

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


@app.route('/esxiglobal', methods=['GET', 'POST'])
def esxiglobal():
    nodeinfo = razor.getNodes()
    form = ESXiGlobalParams(request.form)
    if request.method == 'POST' and form.validate():
        razor.esxi_subnetmask = form.subnetmask.data
        razor.esxi_default_gw = form.default_gw.data
        razor.esxi_dns = form.dns.data
        razor.esxi_domain_suffix = form.domain_suffix.data

        return redirect(url_for('index'))

    return render_template('esxiglobal.html', nodeinfo=nodeinfo, form=form)

@app.route('/nodeidentities', methods=['GET', 'POST'])
def nodeidentities():

    nodeinfo = razor.getNodes()
    form = NodeIdentities(request.form)
    sorted_ru_nodes = razor.getNodesWithRU()

    if len(sorted_ru_nodes) < form.count.data:
        nodecount = len(sorted_ru_nodes)
    else:
        nodecount = form.count.data

    if request.method == 'POST' and form.validate():
        for i in range(0, nodecount):
            octet = int(extractLastOctet(form.starting_ip.data)) + i
            hostid = int(form.first_hostname_id.data) + i
            slen = len(form.first_hostname_id.data)
            while(len(str(hostid)) < slen):
                hostid = '0' + str(hostid)
            hostname = form.hostname_prefix.data + hostid
            ip = (extractSubnet(form.starting_ip.data)) + str(octet)

            razor.updateMeta(sorted_ru_nodes[i], 'HZ_ipaddress', ip)
            razor.updateMeta(sorted_ru_nodes[i], 'HZ_hostname', hostname)

        return redirect(url_for('index'))

    return render_template('nodeidentities.html', nodeinfo = nodeinfo, form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
