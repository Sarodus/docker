import requests

from flask import request, current_app, abort, render_template, session, redirect, jsonify, g
from ..extensions import db
from ..models import Creation, Page
from ..utils import add_js, add_css, add_meta
from ..views.component import Component


class MyCreations:
    """Manage creations"""

    def __init__(self, app=None):
        self.creations = {}

    def init_app(self, app=None):
        pass

    def load_all_creations(self):
        """Debug purpose, in with lot of creations this would take a while!"""
        for creation in Creation.query.all():
            self._add_creation(creation)

    def _add_creation(self, creation):
        """ Helper to add portals to self.creations """

        my_creation = MyCreation(creation)
        self.creations[creation.domain] = my_creation
        return my_creation

    def get_current(self, page):
        domain = request.host[:request.host.index(':')] if ':' in request.host else request.host

        if domain.endswith('.docker'):
            domain = domain.rpartition(".")[0]

        my_creation = self.get_creation(domain) or abort(404, 'No active creation found with domain %s' % domain)
        return my_creation.get_current(page)

    def get_creation(self, domain):
        """Gets the portal from self.creations or adds it if found in the DB.
        :return: portal if found None instead.
        """
        my_creation = self.creations.get(domain)

        if my_creation is None:
            creation = Creation.query.filter_by(domain=domain).first() or abort(404, 'No creation found with domain %s' % domain)
            my_creation = self._add_creation(creation)

        return my_creation


class MyCreation(object):
    """Portal class"""

    base_meta = []

    base_js = [
        '/vendor/jquery/dist/jquery.min.js',
        '/vendor/bootstrap/dist/js/bootstrap.min.js',
        '/vendor/jquery_lazyload/jquery.lazyload.js',
        '/vendor/html5shiv/dist/html5shiv-printshiv.js',
        '/init.js',
        '/general.js',
        '/ajax-intercept.js',
    ]

    base_css = [
        '/vendor/bootstrap/dist/css/bootstrap.min.css',
        '/vendor/bootstrap-ms/bootstrap_ms.css',
        '/main.css',
        '/transition.css',
    ]

    def __init__(self, creation):
        self.creation = creation

    def __repr__(self):
        return u'<MyCreation(%s)>' % self.creation.domain

    def get_current(self, page):
        """The first request of the domain, loads the creation config,
        consequent requests only check if is modified.


        Sets on Flask.g:
            .current_page = models.main.Page
            .page = str
            .slug = str or None
            .wrapper = str
            .css/g.js = list(str)
        """

        if not self.creation.active:
            current_app.logger.warning('Trying to access %s. Is not active.', self)
            abort(404, 'This creation is not longer active')

        current_page = None

        if page:
            current_page = Page.query.filter_by(creation=self.creation, name=page).first()

        if current_page is None:
            current_page = Page.query.filter_by(creation=self.creation).first()

        if current_page is None:
            current_app.logger.error('Page %s not found!' % page)
            abort(404)

        g.current_page = current_page
        g.page = current_page.name

        if request.is_xhr:
            return self

        # TODO, extend with design/page custom
        g.js = list(self.base_js)
        g.css = list(self.base_css)
        g.meta = list(self.base_meta)

        return self

    def render(self):
        return render_template('wrapper.html',
            body = self._parse_components(g.current_page.components)
        )

    def _parse_components(self, components):
        """Exec Component.render() and pass all components rendered to wrapper"""

        result = ''

        for component in components:
            result += Component._get_instance(component.type)._load_config(component)._default()

        return result
