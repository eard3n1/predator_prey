from flask import Flask, render_template, jsonify
from simulation.engine import Simulation
from config import GRID_SIZE

app = Flask(__name__, template_folder="templates", static_folder="static")
engine = Simulation()

@app.route("/")
def index():
    return render_template("index.html", grid_size=GRID_SIZE)

@app.route("/state")
def state():
    return jsonify(engine.get_grid_state())

@app.route("/step")
def step():
    engine.update()
    return jsonify({"status": "ok"})

@app.route("/reset")
def reset():
    engine.__init__()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)
