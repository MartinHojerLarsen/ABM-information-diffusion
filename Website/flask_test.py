from flask import Flask, render_template
from markupsafe import escape

# Commands to run server: 
# $env:FLASK_APP = "hello"
# flask run
# site runs on http://127.0.0.1:5000/ 

app = Flask(__name__)

app.run(debug=True)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/test")
def test():
    return "<p>test</p>"




