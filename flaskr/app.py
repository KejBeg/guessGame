from flask import Flask, redirect, render_template

app = Flask(__name__)



@app.route("/")
def index():
    numOfRows = range(10)
    numOfInputs = range(4)
    return render_template("/index.html", numOfRows=numOfRows, numOfInputs=numOfInputs)