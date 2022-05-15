from flask import redirect, request, render_template, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('log_and_reg.html')

@app.route("/users/login", methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    user_data = {
        'email': request.form['email']
    }
    user = User.get_by_email(user_data)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            return redirect("/")
        session['user_id'] = user.id
        flash("Login Successful", "success")
        return redirect("/dashboard")
    return redirect("/")

@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
        }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')