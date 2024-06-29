from flask_wtf import FlaskForm
from flask import Flask, render_template, request
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = 'mysecret'

todos = ["Learn Flask", "Set up venv", "Buid a cool app"]

class TodoForm(FlaskForm):
    todo = StringField("Todo")
    submit = SubmitField("Add Todo")

@app.route('/', methods=["GET", "POST"])
def index():
    if 'todo' in request.form: #if a post request is made and has a 'todo' attribute
        todos.append(request.form['todo'])
    return render_template('index.html', todos=todos, template_form = TodoForm())

