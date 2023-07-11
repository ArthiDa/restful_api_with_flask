from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

fake_db = {
    1:{'name': 'Clean Car'},
    2:{'name': 'Write Blog'},
    3:{'name': 'Start Stream'},
}

task_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name

class Items(Resource):
    @marshal_with(task_fields)
    def get(self):
        tasks = Task.query.all()
        return tasks
        # return fake_db

    @marshal_with(task_fields)
    def post(self):
        data = request.json
        task = Task(name=data['name'])
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks
        # item_id = len(fake_db.keys()) + 1
        # fake_db[item_id] = {'name': data['name']}
        # return fake_db

class Item(Resource):
    @marshal_with(task_fields)
    def get(self,pk):
        task = Task.query.filter_by(id=pk).first()
        return task
        # return fake_db[pk]
    
    @marshal_with(task_fields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data['name']
        db.session.commit()
        return task
        # fake_db[pk]['name'] = data['name']
        # return fake_db
    
    @marshal_with(task_fields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks
        # del fake_db[pk]
        # return fake_db
    
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

def create_db():
    with app.app_context():
        db.create_all()

if __name__=='__main__':
    create_db()
    app.run(debug=True)