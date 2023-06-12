from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import random
import sqlite3


# Configuring FLASK
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMAMENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Init sqlite
con = sqlite3.connect("scoreboard.db", check_same_thread=False)
cur = con.cursor()

# Creating table if one was not created
tableName = "scoreboard"
cur.execute("CREATE TABLE IF NOT EXISTS scoreboard (id INTEGER PRIMARY KEY,name TEXT, wonState ID,tryCount INT, winningCode INT)")

# Variables
enabledInput = 0 # Var to know with which row we deal
numOfRows = 10 # Declare a number of rows
numOfInputs = 4 # Declare a number for inputs
rangeOfRows = range(numOfRows) # Create a range of rows
rangeOfInputs = range(numOfInputs) # Create a range of inputs

# Generate code
def codeGeneration():
    global gameCode
    gameCode = [None for i in range(numOfInputs)]
    for i in range(numOfInputs):
        gameCode[i] = random.randrange(1, 8)
        while gameCode[i] in gameCode[0:i]:
            gameCode[i] = random.randrange(1, 8)
    print(gameCode)
 
codeGeneration()
 
# Setting the code user should guess
minValue = 1
maxValue = 8


allSubmittedCodes = [[0]*numOfInputs for i in rangeOfRows] # Create a 2d array for all of the codes user submitted
correctPlaces = [0 for i in rangeOfRows] # Create an array for every row that shows how many letters user got right
wrongPlaces = [0 for i in rangeOfRows] # Create an array for every row that shows how many letter user got right but in wrong place


@app.route("/")
def index():
    # Globalize vars for use in rendering the template
    global rangeOfRows
    global rangeOfInputs
    global correctPlaces

    return render_template("/index.html", numOfRows=rangeOfRows, numOfInputs=rangeOfInputs, enabledInput=enabledInput,\
    correctPlaces=correctPlaces, wrongPlaces=wrongPlaces, allSubmittedCodes=allSubmittedCodes, loginName=session.get("loginName"))


@app.route("/scoreboard")
def scoreboard():
    # Define undesirable character
    charsToReplace = [",", "'", "(", ")"] 

    # Define name for scoreboard
    cur.execute("SELECT name FROM scoreboard WHERE wonState = '1';")
    scoreboardNames = list(cur.fetchall())
    # Loop to remove undesirable characters
    for i in range(len(scoreboardNames)):
        scoreboardNames[i] = str(scoreboardNames[i])
        for char in charsToReplace:
            scoreboardNames[i] = scoreboardNames[i].replace(char, "")

    # Define amount of tries for scoreboard
    cur.execute("SELECT tryCount FROM scoreboard WHERE wonState = '1';")
    scoreboardAmountOfTries = list(cur.fetchall())
    # Loop to remove undesirable characters
    for i in range(len(scoreboardAmountOfTries)):
        scoreboardAmountOfTries[i] = str(scoreboardAmountOfTries[i])
        for char in charsToReplace:
            scoreboardAmountOfTries[i] = scoreboardAmountOfTries[i].replace(char, "")
    
    # define the winning code for scoreboard
    cur.execute("SELECT winningCode FROM scoreboard WHERE wonState = '1';")
    scoreboardWinningCode = list(cur.fetchall())
    # Loop to remove undesirable characters
    for i in range(len(scoreboardWinningCode)):
        scoreboardWinningCode[i] = str(scoreboardWinningCode[i])
        for char in charsToReplace:
            scoreboardWinningCode[i] = scoreboardWinningCode[i].replace(char, "")

    return render_template("/scoreboard.html",scoreboardNames=scoreboardNames,\
    scoreboardAmountOfTries=scoreboardAmountOfTries, scoreboardWinningCode=scoreboardWinningCode, maxTries=numOfRows)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return redirect("/")
    if not request.form.get("login-name"):
        session["errorMessage"] = "Login name was not provided"
        return redirect("/error")
    session["loginName"] = request.form.get("login-name")
    return redirect("/") 

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method != "POST":
        return redirect("/")
    session["loginName"] = None
    return redirect("/")

@app.route("/verify", methods=["POST", "GET"])
def verify():
    # Globalize vars for later use in the function
    global enabledInput
    global rangeOfInputs
    global allSubmittedCodes

    # Declare a local submittedCode var
    submittedCode = allSubmittedCodes[enabledInput]
    
    for i in rangeOfInputs:
        # Assigns the requested letters to our var
        try:
            submittedCode[i] = int(request.form.get(f"letter-input-{enabledInput}-{i}"))
        except:
            session["errorMessage"] = "Atleast one input is missing"
            return redirect("/error")
        # Check if user has inputted into every input 
        
        # Check if user
        if submittedCode[i] < minValue or submittedCode[i] > maxValue:
            session["errorMessage"] = "You have tampered with JS or HTML"
            return redirect("/error")
        
        # Checks the values and increments correctPlaces
        if submittedCode[i] == gameCode[i]:
            correctPlaces[enabledInput]+=1 

        # Checks the values and increments wrongPlaces
        if submittedCode[i] in gameCode:
            wrongPlaces[enabledInput]+=1 
    
    # Makes sure the wrongsPlaces arent over the logical max
    wrongPlaces[enabledInput]-= correctPlaces[enabledInput]
    
    # Saves the user's code to global variable
    allSubmittedCodes[enabledInput] = submittedCode
    
    # Increments the current used row
    enabledInput +=1

    # Getting the name
    global name
    if not session.get("loginName"):
        name = "Anonymous"
    else:
        name = session.get("loginName")

    # Redirects to a Winner page if the game was WON
    gameCodeInt = int(''.join(map(str, gameCode)))
    if gameCode in allSubmittedCodes:
        cur.execute("INSERT INTO scoreboard (name, wonState, tryCount, winningCode) VALUES (?, ?, ?, ?)",\
        (name, 1, enabledInput, gameCodeInt))
        con.commit()
        session["resetState"] = "gameWon"
        return redirect("/reset")
    if 0 not in allSubmittedCodes[len(allSubmittedCodes)-1]:
        cur.execute("INSERT INTO scoreboard (name, wonState, tryCount, winningCode) VALUES (?, ?, ?, ?)",\
        (name, 0, enabledInput, gameCodeInt))
        con.commit()
        session["resetState"] = "gameLost"
        return redirect("/reset")

    # Returns back to index if the game wasnt won
    return redirect("/")    

@app.route("/error")
def error():
    if not session.get("errorMessage"):
        return redirect("/")
    return render_template("/error.html", errorMessage=session["errorMessage"])
    
# TODO
@app.route("/gameWon")
def gameWon():
    if session.get("resetState") != "gameWon":
        return redirect("/")
    session["resetState"] = None
    return render_template("/gameWon.html", loginName=name,\
    gameCode=session.get("gameData")["gameCode"], tryCount=session.get("gameData")["tryCount"],\
    maxTries=session.get("gameData")["maxTries"])

# TODO
@app.route("/gameLost")
def gameLost():
    if session.get("resetState") != "gameLost":
        return redirect("/")
    session.get("resetState") == None
    return render_template("/gameLost.html", loginName=name,\
    gameCode=session.get("gameData")["gameCode"])

@app.route("/reset" )
def reset():
    global allSubmittedCodes
    global correctPlaces
    global wrongPlaces
    global enabledInput

    # Saving the data
    session["gameData"] = {
        "loginName": session.get("loginName"),
        "gameCode": gameCode,
        "tryCount": enabledInput,
        "maxTries": numOfRows,
    }

    # Regenaration of code
    codeGeneration()

    allSubmittedCodes = [[0]*numOfInputs for i in rangeOfRows] 
    correctPlaces = [0 for i in rangeOfRows] 
    wrongPlaces = [0 for i in rangeOfRows] 
    enabledInput = 0
    if session.get("resetState") == "gameLost":
        return redirect("/gameLost")
    elif session.get("resetState") == "gameWon":
        return redirect("/gameWon")
    
    return redirect("/")
