from unittest import result
from flask import Flask, render_template, jsonify, request
from markupsafe import escape

# Commands to run server: 
# $env:FLASK_APP = "flask_test"
# $env:FLASK_ENV = "development"    - debug on, updates changes to .py files automatically
# flask run
# flask run --host=0.0.0.0          - public (so Mads can see)
# site runs on http://127.0.0.1:5000/ 

app = Flask(__name__)

# updates changes to templates (and static files) on refresh
app.config['TEMPLATES_AUTO_RELOAD'] = True

# main 
@app.route("/", methods=["POST", "GET"])
def index():
    # if request.method == "POST": 
    #     a = request.form.get("a")
    #     b = request.form.get("b")
    #     sumAB = str(int(a) + int(b))
    #     print(sumAB)
    #     return render_template('index.html', sumAB = sumAB)

    return render_template('index.html')

# AJAX handling
@app.route("/ajax", methods=["POST",  "GET"])
def ajax(): 
    if request.method == "POST": 
        result = request.get_json()
        print(result)

    htmlresult = {"Processed data": "True"}
    return jsonify(htmlresult)



