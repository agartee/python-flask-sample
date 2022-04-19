from flask import Flask
import os


app = Flask(__name__)


@app.route("/")
def hello():
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