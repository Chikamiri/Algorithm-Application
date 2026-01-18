# Maze Algorithm Visualizer & Benchmarker

A comprehensive Python application for visualizing maze generation and pathfinding algorithms. This tool allows users to interactively watch algorithms in real-time, control execution speed, and perform rigorous benchmarking to analyze algorithmic scalability and efficiency.

## Features

* **Interactive Visualization:** Watch algorithms work in real-time on a customizable grid.
* **MVC Architecture:** Clean separation of concerns using Model-View-Controller pattern.
* **Maze Generators:**
  * Recursive Backtracker
  * Prim's Algorithm
* **Pathfinding Solvers:**
  * Breadth-First Search (BFS)
  * Depth-First Search (DFS)
  * A* Search (A-Star)
  * Dijkstra's Algorithm
  * Wall Follower (Right-Hand Rule)
* **Benchmarking Suite:**
  * **In-App:** Quick comparisons of all solvers on the current grid.
  * **Headless (Script):** Extensive scalability testing across multiple grid sizes (10x10 to 60x60+).
* **Data Analysis:** Automated generation of performance graphs (Time, Path Length, Visited Nodes) to visualize Big-O complexity.

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Algorithm-Application
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *Note: Requires `pygame-ce`, `matplotlib`, and `numpy`.*

## Usage

### 1. Interactive Visualizer

Run the main application:

```bash
python main.py
```

#### Controls

**General:**

* `SPACE`: Pause/Resume visualization.
* `R`: Reset grid (keeps current size).
* `[` / `]`: Decrease/Increase speed (Hold `SHIFT` for larger steps).
* `B`: Toggle Benchmark View.

**Grid Resizing:**

* `Arrow Keys`: Increase/Decrease rows and columns (±5).
* `F1`: Preset Small (15x15).
* `F2`: Preset Medium (30x40).
* `F3`: Preset Large (50x70).

**Algorithms:**

* `1`: Generate Maze (Recursive Backtracker)
* `2`: Generate Maze (Prim's Algorithm)
* `3`: Solve with BFS
* `4`: Solve with DFS
* `5`: Solve with A*
* `6`: Solve with Dijkstra
* `7`: Solve with Wall Follower

### 2. Scalability Benchmarking

To perform an extensive analysis of how algorithms perform as grid size increases:

1. **Run the Benchmark Runner:**

    ```bash
    python benchmark_runner.py
    ```

    This script runs all solvers across grid sizes ranging from 10x10 to 60x60 (configurable) and saves data to `results.csv`.

2. **Analyze Results:**

    ```bash
    python analyze_results.py
    ```

    This reads `results.csv` and generates `benchmark_analysis.png`, plotting:
    * Execution Time (ms) vs Grid Size
    * Path Length vs Grid Size
    * Nodes Visited vs Grid Size

## Project Structure

```txt
├── controller/         # Application logic and event handling
├── model/              # Data structures and algorithms
│   ├── generators/     # Maze generation algorithms
│   └── solvers/        # Pathfinding algorithms
├── view/               # Rendering and UI components
├── main.py             # Entry point
├── benchmark_runner.py # Headless data collection script
└── analyze_results.py  # Data visualization script
```
