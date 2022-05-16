from flask_app import app
from flask import render_template, redirect, request, session
from flask import flash
from flask_app.models.user import User
from flask_app.models.location import Location
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def reg_log():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login or register before proceeding', 'login')
        return redirect('/')

    return render_template('dashboard.html', locations = Location.get_all())


@app.route('/save/trails/<int:api_trail_id>/<string:location_name>')
def stash_trail(api_trail_id, location_name):
    if 'user_id' not in session:
        flash('Please login or register before proceeding', 'login')
        return redirect('/')

    data = {
        'location_name' : location_name
    }
    location_id = Location.get_location_id_by_name(data)

    print(f'++++++++++++++++++++++++++++++++++++++++++++++++location_id:{location_id}')
    data = {
        'api_trail_id' : api_trail_id,
        'location_id' : location_id
    }
    trail_id = User.add_trail(data)

    data = {
        'trail_id' : trail_id,
        'user_id' : session['user_id']
    }
    User.stash_trail(data)

    return redirect(f'/trails/{location_id}')







@app.route('/register', methods=['POST'])
def register():
    
    
    #1. validate the form
    if not User.validate_user_registration(request.form):

        return redirect('/')

    #2. create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #3 put hash into data dictionary
    data = {
        'username' : request.form['username'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    
    return redirect('/dashboard')

# ++++++++++++++++++++++++++++++++++++++++
# login / logout route
@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "username" : request.form["username"] }
    user = User.get_by_username(data)
    # user is not registered in the db
    if not user:
        flash("Invalid Username/Password", 'login')
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user.id
    # never render on a post!!!
    return redirect("/dashboard") 


@app.route('/logout')
def logout():
    if 'user_id' not in session:
        flash('Please login or register before proceeding', 'login')
        return redirect('/')

    session.clear()
    return redirect('/')