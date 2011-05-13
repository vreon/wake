from been.couch import CouchStore
from flask import render_template, abort, request, url_for
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from datetime import datetime
from wake import app

store = CouchStore().load()

@app.route('/')
def wake():
    try:
        before = int(request.args.get('before'))
    except (ValueError, TypeError):
        before = None
    return render_template('stream.html', events=store.collapsed_events(before=before))

@app.route('/<slug>')
def by_slug(slug):
    events = list(store.events_by_slug(slug))
    if not events:
        abort(404)
    return render_template('stream.html', events=events)

@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Posts', feed_url=request.url, url=request.url_root,
                    generator=('Wake', None, None))
    sources = store.get_sources()
    for event in store.events():
        if sources[event['source']].get('syndicate'):
            feed.add(event['title'],
                     unicode(event['content']),
                     content_type='html',
                     author=event.get('author', ''),
                     url=urljoin(request.url_root, url_for('by_slug', slug=event.get('slug', ''))),
                     updated=datetime.fromtimestamp(event['timestamp']),
                     published=datetime.fromtimestamp(event['timestamp']))
    return feed.get_response()
