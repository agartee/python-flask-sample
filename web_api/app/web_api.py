from cgitb import reset
from flask import Flask, request, session
import os


app = Flask(__name__)
app.secret_key = 'the random string'

@app.route("/return-codes")
def index():
    print(f'initial session var: {str(session.get("codes"))}')
    if not session.get("codes"):
        print("populating session var...")
        session["codes"] = request.args.get("codes").split(",")
        print(f'session var: {str(session.get("codes"))}')
    
    codes = session["codes"]
    code = codes.pop(0)
    session["codes"] = codes
    
    print(str(code))
    print(f'session var after pop: {str(session.get("codes"))}')

    if not session["codes"]:
        session.pop("codes")

    print(f'final session var: {str(session.get("codes"))}')
    return f"result: {code}", code


@app.route("/clear")
def clear_session():
    session.pop("codes")
    return "", 201


@app.route("/counter")
def counter():
    counterFileName = f"{get_root_app_dir()}/data/counter.txt"
    counterData = readFile(counterFileName)
    
    counter = 0
    if(counterData != ""):
        counter = int(counterData)

    counter = counter + 1
    writeFile(counterFileName, str(counter))
        
    if(counter % 2) == 0:
        return f"Hello! (counter: {counter})"
    else:
        # the web client should be configured to retry on 500s
        return f"Boo! (counter: {counter})", 500

def readFile(fileName:str):
    if not os.path.exists(fileName):
        return ""

    file = open(f"{fileName}", "r")
    data = file.read()
    file.close()
    return data


def writeFile(fileName:str, content:str):
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    file = open(f"{fileName}", "w")
    file.write(content)
    file.close()


def get_root_app_dir():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(scriptDir, os.pardir))
    return parentDir

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)