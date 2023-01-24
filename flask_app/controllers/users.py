from flask import render_template,redirect,request,session

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
    User.save(data)
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    return render_template("dashboard.html")




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