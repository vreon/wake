from been.couch import CouchStore
from flask import render_template, abort, request, url_for
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from datetime import datetime
from wake import app

store = CouchStore().load()

@app.route('/')
def wake():
    return render_template('stream.html', events=store.collapsed_events())

@app.route('/<year>/<month>/<slug>')
def by_slug(year, month, slug):
    events = list(store.events_by_slug(slug))
    if not events:
        abort(404)
    event = events[0]
    timestamp = datetime.fromtimestamp(event['timestamp'])
    if not timestamp.strftime('%Y') == year or not timestamp.strftime('%m') == month:
        abort(404)
    return render_template('single.html', event=event)

@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Posts', feed_url=request.url, url=request.url_root,
                    generator=('Wake', None, None))
    sources = store.get_sources()
    for event in store.events():
        if sources[event['source']].get('syndicate'):
            timestamp = datetime.fromtimestamp(event['timestamp'])
            year = timestamp.strftime('%Y')
            month = timestamp.strftime('%m')
            url = url_for('by_slug', year=year, month=month, slug=event['slug'])
            feed.add(event['title'],
                     unicode(event['content']),
                     content_type='html',
                     author=event.get('author', ''),
                     url=urljoin(request.url_root, url),
                     updated=datetime.fromtimestamp(event['timestamp']),
                     published=datetime.fromtimestamp(event['timestamp']))
    return feed.get_response()
