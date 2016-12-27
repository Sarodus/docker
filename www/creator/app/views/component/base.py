from os.path import isfile

from flask import current_app, redirect, request, url_for, render_template, g
from flask_classful import FlaskView, route

from ...utils import add_js, add_css
from ...models import Component as ModelComponent


class Component(FlaskView):
    """Component main Class"""

    # FlaskView params
    # route_base = "name_in_route"


    # This will store all __subclasses__ instances, get them with _get_instance('component_type')
    __components = {}

    default_config = dict()
    type = None
    friendly_name = None

    route_prefix = '/<string:page_name>'

    special_methods = {
        "index": ["GET", "POST"],
    }


    @classmethod
    def init_app(cls, app, creator):
        """Initialize routes of all subclasses, `ext.creator` extension is required to make the before_request method,
        Save instances to Component.__components[type] = instance
        """
        cls.creator = creator
        for component in cls.__subclasses__():
            Component.__components[component.type] = component()
            component.register(app)


    @classmethod
    def _get_instance(cls, type):
        """Get the instance of component of `type` provided"""
        try:
            return cls.__components[type]
        except KeyError as e:
            raise NotImplementedError('Component type "%s" is not implemented' % type)


    @classmethod
    def build_rule(cls, rule, method=None):
        """Custom subclass FlaskView, all routes end with /"""
        rule = super(Component, cls).build_rule(rule, method)
        if rule.endswith('/'):
            return rule
        return '%s/' % rule


    def before_request(self, name, *args, **kwargs):
        """Routes inside components exec this function first.
        Get current creation to `g.c` and load current component.
        """
        page = request.view_args.pop('page_name', '')
        g.c = self.creator.get_current(page)

        component = self.get_current()
        self._load_config(component)



    def _load_config(self, component):
        """Load config from the component provided,
        and references it in `g.current_component`
        and `g.current_component_config` also available in self.config

        :param component: an instance of ModelComponent
        """
        g.current_component = component

        cc = dict(self.default_config, **component.config)
        if ':' not in request.endpoint:
            cc.update(component.config.get('cover_config', {}))

        g.current_component_config = cc

        self._load_assets()

        return self


    def _default(self):
        """Router to default function called by / or when listing all components from /section/page/"""
        return self._index()


    def _index(self):
        """Usually the default function, return HTML view"""
        raise NotImplementedError('No _index for component type "%s"' % self.type)


    @property
    def config(self):
        """Reference to `g.current_component_config` previously loaded by _load_config(component)"""
        try:
            return g.current_component_config
        except Exception as e:
            raise Exception('No component loaded to `g.current_component_config`')


    def _load_assets(self):
        """Load the assets from ModelComponent and this class"""
        self._load_assets_cls()


    @classmethod
    def _load_assets_cls(cls):
        """Load assets from this class"""
        cls._load_js()
        cls._load_css()

    @staticmethod
    def _load_js():
        """Load js assets from this class"""

        print('Calculate JS assets')

    @staticmethod
    def _load_css():
        """Load css assets from this class"""
        print('Calculate CSS assets')

    @classmethod
    def get_current(cls):
        """Get current component that is on the current type/page"""

        # TODO, support multi same-type-component on the same page.

        for component in g.current_page.components:
            if component.type == cls.type:
                return component

        current_app.logger.warning('No component type "%s" on this page!', cls.type)
        return ModelComponent(type=cls.type)


    @property
    def base_url(self):
        """The page url this component is located"""
        return url_for('main_view', page = g.page)


    @classmethod
    def get_name(cls):
        """Friendly name for this component to display on Admin"""
        return cls.friendly_name or cls.type


    @property
    def current_view(self):
        """Tries to return the current view function name.
        Otherwise returns `index`

        TODO: otherwise returns _default's target function name.
        """
        try:
            endpoint = request.endpoint.split(':')
            if endpoint[0] == self.__class__.__name__:
                return endpoint[1]
        except IndexError as e:
            pass

        return 'index'


    def paginate(self, page, view='index', **kwargs):
        """Make pagination links.
        Uses the self.current_view as target, this could fail by views calling paginate and have no pagination,
        example: media/view/<id_content>: This have no pagination possible for suggested, `index` will be called.

        :param page: page target
        :param kwargs: extra url_for's params
        """
        return self.url_for(view, p=page, **kwargs)


    @classmethod
    def url_for(cls, name, **kwargs):
        """Relative url_for

        :param name: name of function
        :param kwargs: extra url_for's params
        """
        return url_for('%s:%s' % (cls.__name__, name), **kwargs)


    def _render_template(self, template_name_or_list, **context):
        """Render template/s
        Injects config and component

        :param template_name_or_list: Accepts strings or lists.
                                        String iterate over designs.
                                        Lists iterates over list/designs until it finds one.
        :param context: params to render template with

        """

        return render_template(template_name_or_list,
            config = self.config,
            component = self,
            **context
        )

