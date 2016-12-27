from flask import Flask, render_template, g
from jinja2 import BaseLoader, TemplateNotFound

from .extensions import db, cache, sess, creator, celery
from .views.component import Component
from .utils import add_js, add_css, add_meta


class TemplateDesignLoader(BaseLoader):
    """Given the creatorapp's design of the current domain, try the existing correct template"""

    def __init__(self, loader):
        self.loader = loader

    @staticmethod
    def template_designs(template):
        return (
            '%s/%s' % (g.c.creation.design.name, template),
            '%s/%s' % ('default', template)
        )

    def get_source(self, environment, template):
        # If template starts with `default/`, just load
        if template.startswith('default/'):
            return self.loader.get_source(environment, template)

        # Try all designs
        for t in self.template_designs(template):
            try:
                return self.loader.get_source(environment, t)
            except TemplateNotFound as e:
                pass

        # Allow other designs or base paths, try to load literal template
        return self.loader.get_source(environment, template)


class CreatorApp(Flask):
    def __init__(self, import_name='Creator', *args, **kwargs):
        super(CreatorApp, self).__init__(import_name, *args, **kwargs)

        configure_app(self)
        configure_logging(self)
        configure_extensions(self)
        configure_hook(self)
        configure_routes(self)
        configure_blueprints(self)
        configure_template_filters(self)
        configure_error_handlers(self)

        # Replace jinja loader with the `search template/design` layer
        self.jinja_loader = TemplateDesignLoader(self.jinja_loader)


def configure_app(app):
    app.config.from_object('config.Config')
    app.template_folder = app.config['BASE_DIR'] + 'app/templates/'

def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)

    # flask-cache
    cache.init_app(app)

    # flask-session and flask-cache will use the same connection
    if app.config['SESSION_TYPE'] == app.config['CACHE_TYPE'] == 'redis':
        app.config['SESSION_REDIS'] = app.extensions['cache'][cache]._client

    # flask-session
    sess.init_app(app)

    # Portal configs
    creator.init_app(app)

    # celery
    celery.config_from_object(app.config)

    if app.debug:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)


def configure_blueprints(app):
    # Register components
    Component.init_app(app, creator)


def configure_template_filters(app):

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)

    @app.template_filter()
    def html_to_text(value):
        return strip_tags(value)

    @app.template_filter()
    def ordinal(number):
        """ Outputs the ordinal together with the number, i.e. "1st, 2nd..."
            :param number: number to get the ordinal from.
        """
        _ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])  # some black magic.
        return _ordinal(number)


    @app.template_filter()
    def only_ordinal(number):
        """ Outputs the ordinal for the given number, i.e. "st, nd..."
            :param number: number to get the ordinal from.
        """
        _ordinal = lambda n: "%s" % ("tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])  # some black magic.
        return _ordinal(number)


    @app.template_filter('dictsort_by')
    def dictsort_by(d, order, items = False, skip=True):
        """
            Iterate a dict in order. If k from order not found in d yield rest of d elements.
        :param d: dict to iterate.
        :param order: List with the keys order.
        :param items: flag to return k or (k, v)
        :param skip: only returns d.keys() & order and skips the rest.
        :return: yields each element of the dict in order if possible.
        """
        _d = d.copy()
        while _d:
            for ko in order:
                if ko in _d:
                    v = _d.pop(ko)
                    yield ko if not items else (ko, v)
            if not skip:
                # return the rest of the dict
                yield _d.popitem()[0] if not items else _d.popitem()
            else:
                return

    app.jinja_env.globals.update(
        zip=zip,
        add_js=add_js,
        add_css=add_css,
        add_meta=add_meta,
    )


def configure_logging(app):
    """Configure logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    # NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL
    log_level = logging.DEBUG

    handler = WatchedFileHandler(app.config['LOG_DIR']+'/mcp.log')
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)
    app.logger.debug('App started!')


def configure_hook(app):
    @app.after_request
    def call_after_request_callbacks(response):
        for callback in getattr(g, 'after_request_callbacks', ()):
            callback(response)

        return response


def configure_error_handlers(app):

    @app.errorhandler(404)
    def not_found_404(e):
        msg = getattr(e, 'description', e)
        app.logger.error(msg)
        return render_template('default/404.html', msg=msg), 404

    # TODO, 500


def configure_routes(app):

    @app.route('/', methods=('GET', 'POST'))
    @app.route('/<string:page_name>', methods=('GET', 'POST'))
    def main_view(page_name=None):
        g.c = creator.get_current(page_name)
        return g.c.render()
