from sanic.response import text

class BaseModelView():

    can_list = can_get = can_create = can_update = can_delete = True

    def __init__(self, model):
        super(BaseModelView, self).__init__()
        self.model = model

        self.router_base_map = {
            'GET': self.item_list,
            'POST': self.item_create
        }
        self.router_item_map = {
            'GET': self.item_get,
            'PUT': self.item_update,
            'DELETE': self.item_delete
        }

    def register(self, app, url_prefix=None):
        if url_prefix is None:
            url_prefix = self.get_default_url_prefix()

        for endpoint, route, methods in self.get_routes():
            rule = url_prefix + route
            app.add_route(endpoint, rule, methods)

    def get_routes(self):

        route_base = '' 
        route_base_methods = []

        route_item = '/<id_item:number>'
        route_item_methods = []

        if self.can_list:
            route_base_methods.append('GET')

        if self.can_get:
            route_item_methods.append('GET')

        if self.can_create:
            route_base_methods.append('POST')

        if self.can_update:
            route_item_methods.append('PUT')

        if self.can_delete:
            route_item_methods.append('DELETE')

        if route_base_methods:
            yield self.router_base, route_base, route_base_methods
        
        if route_item_methods:
            yield self.router_item, route_item, route_item_methods


    async def router_base(self, request, *args, **kwargs):
        return self.router_base_map[request.method](request, *args, **kwargs)
    

    async def router_item(self, request, id_item, *args, **kwargs):
        return self.router_item_map[request.method](request, id_item, *args, **kwargs)

    def get_default_url_prefix(self):
        return '/%s' % self.model.__name__.lower()

    def item_list(self, request):
        raise NotImplementedError

    def item_get(self, request, id_item):
        raise NotImplementedError

    def item_create(self, request):
        raise NotImplementedError

    def item_update(self, request, id_item):
        raise NotImplementedError

    def item_delete(self, request, id_item):
        raise NotImplementedError
