from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyCNTf-4ydAa1x2rWmhH7EXbmt7FI7NNtuA",
  "authDomain": "pyrebase-lab.firebaseapp.com",
  "projectId": "pyrebase-lab",
  "storageBucket": "pyrebase-lab.appspot.com",
  "messagingSenderId": "516181230238",
  "appId": "1:516181230238:web:33efb3dac1e952b8b2318f",
  "databaseURL": ""
}
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "itay"




firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_up_with_email_and_password(email, password)
            return render_template(add_tweet.html)
        except:
            error = "authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return render_template(add_tweet.html)
        except:
            error = "authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)