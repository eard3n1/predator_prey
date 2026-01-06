# predator_prey
An ecosystem simulation with a web-based visualization built with **Flask**.

## Overview
Simulates a simple ecosystem where prey & predators interact on a 2D grid. The simulation mimics realistic behaviors such as:

- **Prey**: Wandering & local population density bottleneck
- **Predators**: Hunting & starvation mechanics

There is no general population threshold, configuration carrying capacity only affects local (adjacent squares) making the simulation even more realistic.

## Prerequisites
- Python 3.7+
- Flask

## Running
- Install Flask:
    ```bash
    pip install flask
    ```

- Run the simulation:   
    ```bash
    python app.py
    ```

- Open your browser at: <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a>

# License
MIT License