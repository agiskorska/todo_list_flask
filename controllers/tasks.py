from werkzeug import exceptions
from flask import redirect, url_for
from datetime import date

from db import db 

def index(req):
    return [task for task in db.data], 200

def create(req):
    data = req.form
    print(data)
    today = date.today()
    new_task = {
        'task' : data['task'],
        'description': data['description'],
        'due-date': data['due-date'],
        'id': sorted([task['id'] for task in db.data])[-1] + 1,
        'entry-date': today.strftime("%d-%m-%Y"),
        'entry-time': '00:00'
    }

    db.data.append(new_task)
    return db.data, 200

def show(req, id):
    return find_by_id(id), 200

def update(req, id):
    task = find_by_id(id)
    print(task)
    data = req.form
    new_task = {
        "id": task['id'],
        'task' : data['task'],
        'description': data['description'],
        'due-date': data['due-date'],
        'due-time': '00:00',
        'entry-date': task['entry-date'],
        'entry-time': '00:00'
    }
    print(new_task)
    for key, val in new_task:
        print ('this is key')
        print(key)
        task[key] = val
    return 'amended', 200

def destroy(req, id):
    task = find_by_id(id)
    db.data.remove(task)
    return 'deleted', 200

def find_by_id(id):
    try:
        return next(task for task in db.data if task['id'] == id)
    except:
        raise exceptions("this task doesn't exist")