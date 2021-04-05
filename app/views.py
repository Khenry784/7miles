"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager, bcrypt
from flask import render_template, request, redirect, url_for, flash, session, abort,send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm,RegistrationForm
from app.models import UserProfile
from werkzeug.security import check_password_hash
from app.products.models import AddItem
from app.products.forms import AddItemForm



app.config['UPLOAD_FOLDER'] = './uploads'

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    all_data= AddItem.query.all()

    return render_template('home.html',items= all_data)

@app.route('/dashboard')
def dashboard():
    """Render the website's dashboard page."""
    all_data= AddItem.query.all()
    return render_template('dashboard.html',items=all_data)

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/catalog')

def catalog():
    """Render the website's catalog page."""
    all_data= AddItem.query.all()
    
    return render_template('catalog.html',items= all_data)

@app.route('/cart',methods=['POST','GET'])
def cart():
    """Render the website's Shopping Cart page."""
    if 'ShoppingCart'not in session:
        return redirect(request.referrer)
    return render_template('cart.html')    



@app.route("/manageItem", methods=["GET", "POST"])
def manageItem():
    """Render the website's add new item page."""
    all_data= AddItem.query.all()

    # Instantiate your form class
    form = AddItemForm()

    # Validate file upload on submit
    if request.method == 'POST' and form.validate_on_submit:
        title= request.form['title']
        description=  request.form['description']
        price =  request.form['price']
        
        quantity= request.form['quantity']
            
            # Get file data and save to your uploads folder
            


        item = AddItem(title=title,description=description,price=price,quantity=quantity)
            
        db.session.add(item)
        db.session.commit()

        flash('Item added', 'success')
        return redirect(url_for('manageItem'))

    return render_template('manageItem.html',form = form,items = all_data)



#this is our update route where we are going to update our Item
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        item = AddItem.query.get(request.form.get('id'))
 
        item.title = request.form['title']
        item.description = request.form['description']
        item.price = request.form['price']
       
        item.quantity= request.form['quantity']
        

 
        db.session.commit()
        flash("Item Updated Successfully")
 
        return redirect(url_for('manageItem'))

#This route is for deleting our Item
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    item = AddItem.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item Deleted Successfully")
 
    return redirect(url_for('manageItem'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        
        hash_password= bcrypt.generate_password_hash(form.password.data)
        
        user = UserProfile(first_name=form.f_name.data,last_name=form.l_name.data,username=form.username.data,email=form.email.data,password=hash_password)
        
        db.session.add(user)
        db.session.commit()
            
        flash(f'{form.f_name.data}Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title= "Register Page")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        username = form.username.data
        password = form.password.data
            # Get the username and password values from the form.
        user = UserProfile.query.filter_by(username=username).first()
            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.

        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

                # get user id, load into session
                login_user(user, remember=remember_me)

                flash('Logged in successfully.', 'success')

            
            return redirect( url_for('home'))
        else:
            flash('Username or Password is incorrect.', 'danger')
                    
    flash_errors(form)
    return render_template('login.html', form=form, title= "Login Page")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@app.route("/secure-page")
@login_required
def secure_page():
    return render_template('secure_page.html')    


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/manageItem/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

def get_uploaded_images():
    lst = []
    rootdir = os.getcwd()
    # print rootdir
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            lst.append(file)
    return lst

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
