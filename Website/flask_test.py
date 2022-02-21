from flask import Flask, render_template, jsonify
from markupsafe import escape

# Commands to run server: 
# $env:FLASK_APP = "flask_test"
# flask run
# site runs on http://127.0.0.1:5000/ 

app = Flask(__name__)

# debug on - updates changes to .py files automatically
app.run(debug=True)
# updates changes to templates (and static files) on refresh
app.config['TEMPLATES_AUTO_RELOAD'] = True

# main 
@app.route("/")
def index():
    return render_template('index.html')


#json test
@app.route("/data")
def json_test(): 
    return jsonify(
        name = "Mads",
        age = 42
    )


# test for sub URL - access on http://127.0.0.1:5000/test
@app.route("/test")
def test():
    return "<p>test</p>"


