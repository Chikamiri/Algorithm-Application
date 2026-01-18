import time
import threading
from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar

class BenchmarkService:
    def __init__(self):
        self.is_running = False
        self.progress = 0.0
        self.results = {} # {algo_name: {'time': [], 'visited': [], 'path': []}}
        self.thread = None
        self.status_message = "Ready"
        self.error = None

    def start_benchmark(self, rows=30, cols=40, iterations=5):
        if self.is_running:
            return
        
        self.is_running = True
        self.progress = 0.0
        self.results = {}
        self.status_message = "Initializing..."
        self.error = None
        
        self.thread = threading.Thread(target=self._run, args=(rows, cols, iterations))
        self.thread.daemon = True
        self.thread.start()

    def _run(self, rows, cols, iterations):
        solvers = {
            "BFS": BFS(),
            "DFS": DFS(),
            "AStar": AStar()
        }
        generator = RecursiveBacktracker()
        
        # Initialize results storage
        for name in solvers:
            self.results[name] = {'time': [], 'visited': [], 'path': []}

        total_steps = iterations * len(solvers)
        step_count = 0

        try:
            for i in range(iterations):
                self.status_message = f"Generating Maze {i+1}/{iterations}..."
                # Generate
                grid = Grid(rows, cols)
                gen = generator.generate(grid)
                for _ in gen: pass
                
                start_cell = grid.get_cell(0, 0)
                end_cell = grid.get_cell(cols - 1, rows - 1)
                
                for name, solver in solvers.items():
                    self.status_message = f"Maze {i+1}/{iterations}: Running {name}..."
                    grid.reset_visited()
                    
                    # Timing
                    start_time = time.perf_counter_ns()
                    
                    solve_gen = solver.solve(grid, start_cell, end_cell)
                    path = []
                    try:
                        while True:
                            next(solve_gen)
                    except StopIteration as e:
                        path = e.value
                    
                    end_time = time.perf_counter_ns()
                    duration_ms = (end_time - start_time) / 1_000_000
                    
                    # Metrics
                    path_len = len(path) if path else 0
                    visited_count = sum(1 for col in grid.cells for cell in col if cell.visited_by_solver)
                    
                    # Store
                    self.results[name]['time'].append(duration_ms)
                    self.results[name]['visited'].append(visited_count)
                    self.results[name]['path'].append(path_len)
                    
                    step_count += 1
                    self.progress = step_count / total_steps
            
            self.status_message = "Done"
            
        except Exception as e:
            self.error = str(e)
            self.status_message = f"Error: {str(e)}"
            print(f"Benchmark Error: {e}")
        finally:
            self.is_running = False

    def get_averages(self):
        avgs = {}
        for name, metrics in self.results.items():
            if not metrics['time']:
                continue
            avgs[name] = {
                'time': sum(metrics['time']) / len(metrics['time']),
                'visited': sum(metrics['visited']) / len(metrics['visited']),
                'path': sum(metrics['path']) / len(metrics['path'])
            }
        return avgs
