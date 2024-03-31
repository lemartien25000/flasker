from flask import Flask, render_template


#create a Flask instance
app = Flask(__name__)


#create a route decorator : '/' the homepage
#@app.route('/')
#def index():
#    return "<h1>Hello word!</h1>"

@app.route('/')
def index():
    return render_template('index.html')

# localhost:5000/user/sofiane
@app.route('/user/<name>')
def user(name):
    return "<h1>Hello {}</h1>".format(name)

# Create custom Error pages
# invalide URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# internal server error thing....
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

