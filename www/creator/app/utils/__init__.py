from flask import g

def add_js(js):
    if js not in g.js:
        g.js.append(js)

def add_css(css):
    if css not in g.css:
        g.css.append(css)

def add_meta(meta):
    if meta not in g.meta:
        g.meta.append(meta)
