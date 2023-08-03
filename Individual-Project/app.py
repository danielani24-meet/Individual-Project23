from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os

config = {
  "apiKey": "AIzaSyA8zoHzeFhM63KAv8eQYHqEfxvcfVdWXLM",
  "authDomain": "personal-project23.firebaseapp.com",
  "projectId": "personal-project23",
  "storageBucket": "personal-project23.appspot.com",
  "messagingSenderId": "290604049961",
  "appId": "1:290604049961:web:89972b9fc9be2954ff5e38",
  "measurementId": "G-GBHG3TNSYH", "databaseURL": "https://personal-project23-default-rtdb.firebaseio.com/"
}

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




def upload_file(file):
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(UPLOAD_FOLDER + "/" + filename)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email":request.form["email"], "password":request.form['password']}
            db.child("Users").child(UID).set(user)
            upload_file(photo)
            rating = request.form(rating)
            ref = db.reference('rating')
            new_rating = ref.push({
                'rating': rating
                })
            return redirect(url_for('all_reviews'))
            
        except:
            error = "Authentication failed"
#    redirect
    return render_template("signup.html")

# @app.route('/', methods=['GET', 'POST'])
# def signin():
#     error = ""
#     if request.method =='POST':
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             login_session['user'] = auth.sign_in_user_with_email_and_password(email, password)
#             return redirect(url_for('all_reviews'))
#         except:
#             error = "Authentication failed"
#     return render_template("signin.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('all_reviews'))
    return render_template("signin.html")

@app.route('/main')
def all_reviews():
    reviews = db.child("Reviews").get().val()
    return render_template("main.html", reviews = reviews)
    #????
#def display():
 #   parent_ref = db.reference('parent_node').get().val()
  #  return render_template('main.html', data=parent_ref)
    #????


@app.route('/newreview', methods=['GET', 'POST'])
def new_review():
    error = ""
    if request.method == 'POST':
        # try:  
        UID = login_session['user']['localId']
        photo= request.files['photo']
        review = {"cafesname":request.form['cafesname'], "photo":photo.filename}
        db.child("Reviews").push(review)
        return redirect(url_for('new_review'))

        # except:
        #     error = "Authentication failed"
        #     return render_template("newreview.html")
    else:
        return render_template("newreview.html")








#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)