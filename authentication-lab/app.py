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
  "databaseURL": "https://pyrebase-lab-default-rtdb.firebaseio.com/"
}
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "itay"


user_dict = {"Users": {"Fouad": {"name": "Fouad", "email": "fouad@gmail.com"},  "Aseel": {"name": "Aseel",  "email": "aseel@gmail.com"}}}



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user: {"email": request.form['email'], "password": request.form['password']}
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return render_template("add_tweet.html")
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user: {"email": request.form['email'], "password": request.form['password'], "name" : request.form['full_name'], "username" : 
        request.form['username']}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return render_template("add_tweet.html")
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet = {"title" : request.form['title'], "text" : request.form['text'], "uid" : login_session['user']['localId']}
        login_session['tweet'] = tweet
        db.child("Tweets").push(tweet)
        redirect(url_for('all_tweets'))
        #except:
         #   error = "Somthing went wrong"
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    # tweet = db.child("Tweets").child(login_session['tweet']['localId']).get().val()
    tweet = db.child("Tweets").get().val().values()
    print(tweet)
    return render_template("tweets.html", tweet = tweet)

if __name__ == '__main__':
    app.run(debug=True)