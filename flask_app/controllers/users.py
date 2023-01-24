from flask import render_template,redirect,request,session,flash

from flask_app import app

from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/register',methods=['POST'])
def create():
    if not User.validate_user(request.form):
        return redirect('/')

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pw
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect("/")
    
    #grab the user
    data = {
        'id' : session['user_id']
    }
    logged_user = User.get_one(data)
    return render_template("dashboard.html", logged_user=logged_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    userdb = User.get_by_email(data)
    if not userdb:
        flash("invalid credentials", "log")
        return redirect("/")
    
    if not bcrypt.check_password_hash(userdb.password, request.form['password']):
        flash("invalid credentials", "log")

    session['user_id'] = userdb.id
    return redirect('/dashboard')



@app.route('/users')
def users():
    return render_template("results.html",all_users=User.get_all())


@app.route('/show/<int:user_id>')
def detail_page(user_id):
    data = {
        'id': user_id
    }
    return render_template("details_page.html",user=User.get_one(data))

@app.route('/edit_page/<int:user_id>')
def edit_page(user_id):
    data = {
        'id': user_id
    }
    return render_template("edit_page.html", user = User.get_one(data))

@app.route('/update/<int:user_id>', methods=['POST'])
def update(user_id):
    data = {
        'id': user_id,
        "fname":request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email']
    }
    User.update(data)
    return redirect("/users")

@app.route('/delete/<int:User_id>')
def delete(User_id):
    data = {
        'id': User_id,
    }
    User.destroy(data)
    return redirect('/users')