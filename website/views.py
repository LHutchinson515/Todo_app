from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .models import Todo
from . import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    message = request.args.get('message', None)
    return render_template("index.html", todo_list=todo_list, message = message)


@my_view.route("/add", methods=["POST"])
def add():
    try:
        task= request.form.get("task")
        new_todo = Todo (task=task)
        db.session.add (new_todo)
        db.session.commit()
        return redirect(url_for ("my_view.home"))
    except:
        message = "This task is already existing, please try to add another task or mark the existing as complete if need be"
        return redirect(url_for("my_view.home", message = message))


@my_view.route("/update/<todo_id>")
def update (todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete 
    db.session.commit() 
    return redirect (url_for("my_view.home"))


@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by (id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))
