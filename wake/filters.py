import time
from datetime import datetime
from twitter_text import TwitterText
from flask import Markup

def relative_time(timestamp):
    delta = (datetime.now() - datetime.fromtimestamp(timestamp))
    delta_s = delta.days * 86400 + delta.seconds
    if delta_s < 60:
        return "less than a minute ago"
    elif delta_s < 120:
        return "about a minute ago"
    elif delta_s < (60 * 60):
        return str(delta_s / 60) + " minutes ago"
    elif delta_s < (120 * 60):
        return "about an hour ago"
    elif delta_s < (24 * 60 * 60):
        return "about " + str(delta_s / 3600) + " hours ago"
    elif delta_s < (48 * 60 * 60):
        return "1 day ago"
    else:
        return str(delta_s / 86400) + " days ago"

def absolute_time(timestamp):
    return time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime(timestamp))

def markup_tweet(text):
    return Markup(TwitterText(text).autolink.auto_link())
