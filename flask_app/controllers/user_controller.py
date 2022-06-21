
from flask_app import app
from flask import flash 
from flask import redirect, render_template, request, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
bcrypt = Bcrypt(app)


# ============================ DISPLAY ROUTES =======================================
@app.route("/")
def display_form():
    if "user_id" in session:
        return redirect ('/')

    return render_template("form.html")

@app.route("/dashboard")
def display_dashboard():
    if "user_id" not  in session:
        return redirect ('/')
    data = {
        'id':session['user_id']
    }
    one_user=User.get_one(data)
    return render_template("dashboard.html", one_user=one_user)


# ============================ DISPLAY ROUTES =======================================
# ============================ FORM ROUTES =========================================


@app.route("/register/user", methods=['POST'])
def register_form():
    if not User.validate_registracion(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data ={
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    print(data)
    session['user_id'] = User.create_one(data)
    return redirect("/dashboard")
    

@app.route("/login", methods=["POST"])
def login_form():
    data ={
        'email' : request.form['email'],
    }
    one_user = User.get_by_email(data)
    if not one_user:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
    # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = one_user.id
    return redirect("/dashboard")

@app.route('/logout')
def logout ():
    session.clear()
    return redirect('/')






# ============================ FORM ROUTES =========================================



