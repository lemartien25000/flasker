from dotenv import load_dotenv
load_dotenv()
import pymysql 
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from datetime import datetime
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#create a Flask instance
app = Flask(__name__)
# add database
# Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
# 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ghost25000$@localhost/our_users'
app.config['SECRET_KEY'] = "ghost@25000$"
# Initialize the database
db = SQLAlchemy(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Flask Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username ?", validators=[DataRequired()])
    password = PasswordField("Password ?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Login Page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login successfully!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password - Try again.")
        else:
            flash("That user does'nt exists! - Try again. ")

    return render_template('login.html', form=form)
 
# Create Logout Page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logget out.")
    return redirect(url_for('login'))
    

# Create dashboard Page = Tableau de bord
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    record_to_update = Users.query.get_or_404(id)
    our_users = Users.query.order_by(Users.date_added) 
    if request.method == 'POST':
        record_to_update.name = request.form['name']
        record_to_update.email = request.form['email']
        record_to_update.phone = request.form['phone']
        record_to_update.favourite_color = request.form['favourite_color']
        record_to_update.ville = request.form['ville']
        record_to_update.statut = request.form['statut']
        record_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("dashboard.html",form=form,record_to_update=record_to_update,our_users=our_users, id=id)
        except:
            flash("Error! looks like there was a problem... try again")
            return render_template("dashboard.html",form=form,record_to_update=record_to_update,our_users=our_users, id=id)
    else:
        return render_template("dashboard.html",form=form,record_to_update=record_to_update,our_users=our_users, id=id)

    return render_template('dashboard.html')


# Create a Blog Post
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))


# create Model
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    favourite_color = db.Column(db.String(120))
    ville = db.Column(db.String(50))
    statut = db.Column(db.String(10))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # do some password stuff
    
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    # create a String
    def __repr__(self):
        return '<Name %r>' %self.name

# Create a password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What is your email ?", validators=[DataRequired()])
    password_hash = PasswordField("What is your password ?", validators=[DataRequired()])
    submit = SubmitField("Submit") 

# Create a Name Form Class
class NamerForm(FlaskForm):
    name = StringField("What is your name ?", validators=[DataRequired()])
    submit = SubmitField("Submit") 

class UserForm(FlaskForm):
    name = StringField("Name ?", validators=[DataRequired()])
    username = StringField("Username ?", validators=[DataRequired()])
    email = StringField("Email ?", validators=[DataRequired()])
    phone = StringField("Phone ?")
    favourite_color = StringField("Favourite color ?")
    ville = SelectField("Ville ?", choices=[('constantine','Constantine'),('annaba','Annaba'),('alger','Alger'),('oran','Oran')], validators=[DataRequired()], default='constantine')
    statut = RadioField("Statut ?", choices=[('privé','Privé'),('public','Public')], validators=[DataRequired()], default='privé')
    password_hash = PasswordField('Password ?', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must mach!')])
    password_hash2 = PasswordField('Confirm password ?', validators=[DataRequired()])
    submit = SubmitField("Submit") 

#Create a Post Form
class PostForm(FlaskForm):
    title = StringField("Title ?", validators=[DataRequired()])
    content = StringField("Content ?", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author ?", validators=[DataRequired()])
    slug = StringField("Slug ?", validators=[DataRequired()])
    submit = SubmitField("Submit") 

# Add Post Page
@app.route('/add_post', methods=['GET','POST'])
@login_required # pour obliger l'utilisateur a s'authentifier avant d'ajouter un post.
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        # Add Post data to the database
        db.session.add(post)
        db.session.commit()
        flash("Blog Post submitted successfully...")
        # Redirect to th web page
    return render_template('add_post.html', form=form)

# Create Post Page
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# Create Edit Post 
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required  # seuls les users authentifiés peuvent acceder a cette fonction edit_post(id)
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # update database : Posts Table
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)


    return render_template('post.html', post=post)

# deleting Blog Post 
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
       db.session.delete(post_to_delete)
       db.session.commit()
       flash("Blog Post was deleting !")
       posts = Posts.query.order_by(Posts.date_posted)
       return render_template('posts.html', posts=posts)
    except:
       flash("Whoops there was a problem deleting post, try again !")
       posts = Posts.query.order_by(Posts.date_posted)
       return render_template('posts.html', posts=posts)


# Create Posts Page
@app.route('/posts')
def posts():
    # grab all the posts from table posts in the database our_users
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)

# create a JSON thing for example
@app.route('/date')
def get_current_date():
    notes = {
        "sofiane":"15",
        "riad":"17",
        "manel":"10"
    }
    return notes
    #return { "DATE":date.today()}
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!!")
        our_users = Users.query.order_by(Users.date_added)        
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash("Woops there is a problem deleting user!!!, try again.")
        our_users = Users.query.order_by(Users.date_added)        
        return render_template('add_user.html', form=form, name=name, our_users=our_users)        


# Update Database record
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()
    record_to_update = Users.query.get_or_404(id)
    our_users = Users.query.order_by(Users.date_added) 
    if request.method == 'POST':
        record_to_update.name = request.form['name']
        record_to_update.email = request.form['email']
        record_to_update.phone = request.form['phone']
        record_to_update.favourite_color = request.form['favourite_color']
        record_to_update.ville = request.form['ville']
        record_to_update.statut = request.form['statut']
        record_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("update.html",form=form,record_to_update=record_to_update,our_users=our_users, id=id)
        except:
            flash("Error! looks like there was a problem... try again")
            return render_template("update.html",form=form,record_to_update=record_to_update,our_users=our_users, id=id)
    else:
        return render_template("update.html",form=form,record_to_update=record_to_update,our_users=our_users, id=id)

#create a route decorator : '/' the homepage
#@app.route('/')
#def index():
#    return "<h1>Hello word!</h1>"

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    # creation form depuis class UserForm
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hash password and put it in the table
            hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            user = Users(username=form.username.data,name=form.name.data, email=form.email.data,phone=form.phone.data,favourite_color=form.favourite_color.data,ville=form.ville.data,statut=form.statut.data,password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''
            form.phone.data = ''
            form.favourite_color.data = ''
            form.ville.data = 'Constantine'
            form.statut.data = 'privé'
            form.password_hash.data = ''
            flash("User added successfully...")
        else:
            flash("Email already exists!!!")
        
    our_users = Users.query.order_by(Users.date_added)        
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


@app.route('/')
def index():
    flash("Welcome to our webpage.")
    return render_template('index.html')

# localhost:5000/user/sofiane
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

# Create custom Error pages
# invalide URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# internal server error thing....
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

# create password test page
@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #Look up user by email address
        pw_to_check = Users.query.filter_by(email=email).first()
        #Check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)
        # clear the Passwordform
        form.email.data = ''
        form.password_hash.data = ''
    return render_template("test_pw.html", 
                        email=email, 
                        password=password, 
                        pw_to_check=pw_to_check, 
                        passed=passed, 
                        form=form)
        

# create name page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully!")
    return render_template("name.html", name=name, form=form)
        

# si on souhaite acceder a cette application via navigateur d'un autre pc
# du réseau il faut renommer hello.py en app.py et ajouter les 2 lignes de code
# ainsi, depuis un autre pc, on lance le navigateur et on tape 192.168.1.10:5000
#if __name__ == '__main__':
#    app.run(host='192.168.1.10', port=5000)

