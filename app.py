from flask import Flask, request, render_template, Response
from flask_restful import Resource, Api
from jinja2.runtime import identity

import todo
from main import user_list

app = Flask(__name__)
api = Api(app)



class ListItems(Resource):

        def get(self):
                user_list = todo.TodoList()
                user_list.load()
                json_list = [item.as_json() for item in user_list]
                return Response(render_template('show_list.html', json_list=json_list), mimetype='text/html')

        def post(self):
                user_list = todo.TodoList()
                user_list.load()
                loc = int(request.form.get('id'))-1
                priority = request.form.get('Priority', default=user_list[loc].priority)
                if type(priority) == int:
                        user_list[loc].update('priority', priority)
                done = request.form.get('Done', default=user_list[loc].done)
                done = True if done == 'on' else False
                user_list[loc].update('done', done)
                due = request.form.get('Due', default=user_list[loc].due)
                if len(due) > 1:
                        user_list[loc].update('due', due)
                desc = request.form.get('Description', default=user_list[loc].note)
                if len(desc) > 1:
                        user_list[loc].update('note', desc)
                user_list.save()
                json_list = [item.as_json() for item in user_list]
                return  Response(render_template('show_list.html', json_list=json_list), mimetype='text/html')


class AddItem(Resource):

        def get(self):
                return Response(render_template('new_item.html'))

        def post(self):
                priority = request.form.get('Priority', default=0)
                done = request.form.get('Done', default=False)
                done = True if done == 'on' else False
                due = request.form.get('Due', default=None)
                desc = request.form.get('Description', default='')
                user_list = todo.TodoList()
                user_list.load()
                user_list.add(desc,priority,due,done)
                user_list.save()
                json_list = [item.as_json() for item in user_list]
                return Response(render_template('show_list.html', json_list=json_list))


class ChangeItem(Resource):

        def post(self):
            to_change = int(request.form.get('to_change'))-1
            user_list = todo.TodoList()
            user_list.load()
            item = user_list[to_change]
            return Response(render_template('change_item.html', item=item))

api.add_resource(ListItems, '/')
api.add_resource(AddItem, '/add_item')
api.add_resource(ChangeItem, '/change_item')


if __name__ == "__main__":
        app.run(debug=True, port=5000)