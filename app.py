import os
from flask import Flask, render_template
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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
