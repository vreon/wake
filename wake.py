import couchdb
from been.couch import CouchStore

from flask import Flask, render_template
app = Flask(__name__)

store = CouchStore()
store.load()

@app.route('/')
def wake():
    return render_template('stream.html', events=store.events())

if __name__ == '__main__':
    app.run(debug=True)