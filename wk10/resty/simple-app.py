from flask import Flask
from flask_restful import Resource, Api, abort, request

app = Flask(__name__)
api = Api(app)

resource_store = [{
  'id': 1,
  'description': 'some widget'
}]

class WidgetList(Resource):
  def get(self):
    return resource_store, 200
  def post(self):
    resource_store.append(request.json)
    return 'created', 201

class Widget(Resource):
  def get(self, resource_id):
    resources = [x for x in resource_store if x['id'] == resource_id]
    if len(resources) == 0:
      abort(404, message=f'widget with id {resource_id} does not exist')
    else:
      return resources[0], 200
  def put(self, resource_id):
    resource_indexes = [(i, item) for (i,item) in enumerate(resource_store) if item['id'] == resource_id]
    if len(resource_indexes) == 0:
      abort(404, message=f'widget with id {resource_id} does not exist')
    else:
      index = resource_indexes[0][0]
      resource_store[index]['description'] = request.json['description']
      return 'accepted', 202
  def delete(self, resource_id):
    resource_indexes = [(i, item) for (i,item) in enumerate(resource_store) if item['id'] == resource_id]
    if len(resource_indexes) == 0:
      abort(404, message=f'widget with id {resource_id} does not exist')
    else:
      index = resource_indexes[0][0]
      del resource_store[index]
      return 'accepted', 202

api.add_resource(WidgetList, '/widgets')
api.add_resource(Widget, '/widgets/<int:resource_id>')

if __name__ == '__main__':
  app.run(debug=True)