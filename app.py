from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
from controllers import tasks
from db import db 

app = Flask(__name__)
CORS(app)

@app.route('/')
def welcome():
    return "Welcome to my task manager. Please sit back and relax."

@app.route('/tasks/', methods = ['GET', 'POST'])
def show_tasks():
    fns = {
        'GET': tasks.index,
        'POST': tasks.create
    }
    resp, code = fns[request.method](request)
    return render_template('all_tasks.html', page_title= 'Tasks for today', tasks=db.data), code

@app.route('/tasks/<int:task_id>', methods = ['GET', 'PUT', 'POST'])
def tasks_handler(task_id):
    fns = {
        'GET': tasks.show,
        'POST': tasks.destroy
    }
    resp, code = fns[request.method](request, task_id)
    if resp == 'deleted':
        return redirect(url_for('show_tasks'))
    return resp, code

@app.route('/update/<int:task_id>', methods = ['POST'])
def update_tasks(task_id):
    resp, code = tasks.update(request, task_id)
    return redirect(url_for('show_tasks')), code

if __name__ == '__main__':
    app.run(debug=True)