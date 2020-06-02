from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys 


app = Flask(__name__) #creates an application that is named after the file 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sean_mei@localhost:5432/todoapp'; #SQLAlchemy cannot create your database for 
                                                                                        #you so we have to do it manually from terminal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model): #create table  (parent)
    __tablename__ = 'todos' # names it togo 
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False,  default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable = False) 

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model): #(child)
    __tablename__ ='todolist'
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable= False, default = False )
    todos = db.relationship('Todo', backref='list', lazy =True )

@app.route('/todos/create', methods=['POST']) #new route that searches for Post request 
def create_todo(): 
    error =False
    body = {}
    print("DAF")
    try: 
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo (description= description, completed = False) # makes a todo object 
       
        active_list = TodoList.query.get(list_id)
        todo.list = active_list
        
        
        db.session.add(todo) #pednding 
        db.session.commit() # commit to db
        body['description'] = todo.description

    except:
        error = True 
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (500)
    else:
        return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id): #method takes a paramaters that we defined in the route 
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/lists/<list_id>/')
def get_list_todos(list_id):
    return render_template('index.html',
    active_list=TodoList.query.get(list_id),
    lists= TodoList.query.order_by('id').all(),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    ) 

@app.route('/todo/createlist', methods=['POST'] )
def create_List():
    error = False
    bod = {}
    print("HELLO")
    try:
        names = request.get_json()['name']
        List = TodoList (name=names)
        db.session.add(List)
        db.session.commit() # commit to db
        bod['names'] = List.name
        bod['id'] = List.id
        print('fuck bitches get money' , bod)
    except:
        print("BYE")
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (500)
    else:
        return jsonify(bod)

@app.route('/todoslist/<todo_id>', methods=['DELETE'])
def delete_list(todo_id):
    try:
        TodoList.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/set-completed-lists', methods=['POST'])
def set_completed_todo_list(todo_id): #method takes a paramaters that we defined in the route 
    try:
        completed = request.get_json()['completed']
        todo = TodoList.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return '' 
        
@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id =1 ))


       
