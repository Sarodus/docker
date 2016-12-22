from sanic.response import text, json
from ..base import BaseModelView

class ModelView(BaseModelView):

    def __init__(self, model, session):
        super(ModelView, self).__init__(model)
        self.session = session

    def get_default_url_prefix(self):
        return '/%s' % self.model.__tablename__

    def item_list(self, request):
        sess = self.session()
        items = list(map(lambda u: u.serialize(), sess.query(self.model)))
        return json(items)

    def item_get(self, request, id_item):
        sess = self.session()
        item = sess.query(self.model).get(id_item)
        if item is None:
            return json({'code': 404, 'msg':'Not found'})
        return json(item.serialize())

    def item_create(self, request):
        sess = self.session()
        # TODO, fill item with request.json or request.form or ??
        # TODO, validate
        item = self.model()
        sess.add(item)
        sess.commit()
        return json(item.serialize(), status=201)

    def item_update(self, request, id_item):
        return json({'msg':'Not yet implemented!', 'code': 404})

    def item_delete(self, request, id_item):
        return json({'msg':'Not yet implemented!', 'code': 404})
