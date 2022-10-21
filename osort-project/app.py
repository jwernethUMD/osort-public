from flask import Flask, render_template, request
from osort import PlayerData


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    playerData = []
    stat = "Circle Size"
    playerID = "14981497"
    if request.method == "POST":
        playerID = request.form["playerID"]
        stat = request.form["stat"]
    
    [stat, playerData] = PlayerData(playerID, stat)
        
    return render_template("main-page.html", sortData = playerData, statType = stat, id = playerID)



if __name__ == "__main__":
    app.run(debug=True)