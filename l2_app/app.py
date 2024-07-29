from flask import Flask, render_template, request, url_for
import os
from movies import my_movie_list

app = Flask(__name__)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@app.route("/")
@app.route("/mypage")
def mypage():
    return render_template('mypage.html')

@app.route("/myaccount")
def myaccount():
    return render_template('myaccount.html')

@app.route("/mymovies")
def movies():
    return render_template('mymovies.html', my_movie_list = my_movie_list)

@app.route("/mylearning")
def learning():
    return render_template('mylearning.html')

@app.route("/mymovies/<movie_name>/script")
def display_text(movie_name):
    file_name = movie_name+ ".txt"
    file_path = os.path.join('static','files', file_name)
    with open(file_path, 'r') as file:
        content = file.read()
    return render_template('moviescript.html', movie_name= movie_name, content=content)

@app.route("/mymovies/10_things_i_hate_about_you/vocabulary")
def vocab():
    return render_template("vocabulary.html")

@app.route("/mymovies/10_things_i_hate_about_you/discussionquestions")
def discussion_questions():
    return render_template("discussionquestions.html")

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    answers = {
        "answer1": request.form['answer1'],
        "answer2": request.form['answer2'],
        "answer3": request.form['answer3'],
        # Add more answers as needed
    }
    # Process the answers as needed
    return "Answers submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)