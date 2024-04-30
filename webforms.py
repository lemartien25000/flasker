from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField


# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username ?", validators=[DataRequired()])
    password = PasswordField("Password ?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What is your email ?", validators=[DataRequired()])
    password_hash = PasswordField("What is your password ?", validators=[DataRequired()])
    submit = SubmitField("Submit") 

# Create a Name Form Class
class NamerForm(FlaskForm):
    name = StringField("What is your name ?", validators=[DataRequired()])
    submit = SubmitField("Submit") 

# Create a Search Form Class
class SearchForm(FlaskForm):
    searched = StringField("searched ?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name ?", validators=[DataRequired()])
    username = StringField("Username ?", validators=[DataRequired()])
    email = StringField("Email ?", validators=[DataRequired()])
    phone = StringField("Phone ?")
    favourite_color = StringField("Favourite color ?")
    about_author = TextAreaField("About Author ?")
    ville = SelectField("Ville ?", choices=[('constantine','Constantine'),('annaba','Annaba'),('alger','Alger'),('oran','Oran')], validators=[DataRequired()], default='constantine')
    statut = RadioField("Statut ?", choices=[('privé','Privé'),('public','Public')], validators=[DataRequired()], default='privé')
    password_hash = PasswordField('Password ?', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must mach!')])
    password_hash2 = PasswordField('Confirm password ?', validators=[DataRequired()])
    profile_pic = FileField("Profile Picture")
    submit = SubmitField("Submit") 

#Create a Post Form
class PostForm(FlaskForm):
    title = StringField("Title ?", validators=[DataRequired()])
    #content = StringField("Content ?", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('content', validators=[DataRequired()])
    author = StringField("Author ?")
    slug = StringField("Slug ?", validators=[DataRequired()])
    submit = SubmitField("Submit") 

