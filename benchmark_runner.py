import time
import csv
from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar
from model.solvers.dijkstra import Dijkstra
from model.solvers.wall_follower import WallFollower

def run_benchmark(sizes=[10, 20, 30, 40, 50], iterations=10):
    solvers = {
        "BFS": BFS(),
        "DFS": DFS(),
        "AStar": AStar(),
        "Dijkstra": Dijkstra(),
        "WallFollower": WallFollower()
    }
    
    generator = RecursiveBacktracker()
    
    results = []
    
    print(f"Starting Scalability Benchmark...")
    
    for size in sizes:
        rows, cols = size, size
        print(f"Testing {cols}x{rows} grid...")
        
        for i in range(iterations):
            # Generate a new maze for each iteration
            grid = Grid(rows, cols)
            gen = generator.generate(grid)
            for _ in gen: pass # Run to completion
            
            start_cell = grid.get_cell(0, 0)
            end_cell = grid.get_cell(cols - 1, rows - 1)
            
            for name, solver in solvers.items():
                grid.reset_visited()
                
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
                path_len = len(path) if path else 0
                
                # Count how many cells were visited by solver
                visited_count = sum(1 for col in grid.cells for cell in col if cell.visited_by_solver)
                
                results.append({
                    "size": size,
                    "iteration": i,
                    "algorithm": name,
                    "time_ms": duration_ms,
                    "path_len": path_len,
                    "visited_count": visited_count
                })
            
    # Save to CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["size", "iteration", "algorithm", "time_ms", "path_len", "visited_count"])
        writer.writeheader()
        writer.writerows(results)
    
    print("Benchmarking complete. Results saved to results.csv")

if __name__ == "__main__":
    # For a quick test, use fewer iterations and smaller sizes
    run_benchmark(sizes=[50, 100, 500, 1000, 5000, 10000], iterations=50)