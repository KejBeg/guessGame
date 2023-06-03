import game
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMAMENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

gameCode = [1, 2, 3, 4]

enabledInput = 0

numOfRows = 10
numOfInputs = 4
rangeOfRows = range(numOfRows)
rangeOfInputs = range(numOfInputs)
@app.route("/")
def index():
    global rangeOfRows
    global rangeOfInputs
    global correctPlaces
    return render_template("/index.html", numOfRows=rangeOfRows, numOfInputs=rangeOfInputs, enabledInput=enabledInput, correctPlaces=correctPlaces, wrongPlaces=wrongPlaces, allSubmittedCodes=allSubmittedCodes)

allSubmittedCodes = [[0]*numOfInputs for i in rangeOfRows]
correctPlaces = [0 for i in rangeOfRows]
wrongPlaces = [0 for i in rangeOfRows]
@app.route("/verify", methods=["POST", "GET"])
def verify():
    global enabledInput
    global rangeOfInputs
    submittedCode = [0 for i in rangeOfInputs]
    for i in rangeOfInputs:
        submittedCode[i] = int(request.form.get(f"letter-input-{enabledInput}-{i}"))
        if submittedCode[i] == gameCode[i]:
            correctPlaces[enabledInput] = correctPlaces[enabledInput] + 1
        if submittedCode[i] in gameCode:
            wrongPlaces[enabledInput] = wrongPlaces[enabledInput] + 1
    wrongPlaces[enabledInput]-= correctPlaces[enabledInput]
    
    allSubmittedCodes[enabledInput] = submittedCode
    print(allSubmittedCodes)
    enabledInput +=1
    return redirect("/")    
    
@app.route("/gameWon")
def gameWon():
    return render_template("gameWon.html")