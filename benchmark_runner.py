import time
import csv
from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar

def run_benchmark(rows, cols, iterations=10):
    solvers = {
        "BFS": BFS(),
        "DFS": DFS(),
        "AStar": AStar()
    }
    
    generator = RecursiveBacktracker()
    
    results = []
    
    print(f"Running benchmarks on {cols}x{rows} grid, {iterations} iterations...")
    
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
            
            # Count visited nodes
            visited_count = 0
            
            solve_gen = solver.solve(grid, start_cell, end_cell)
            try:
                while True:
                    next(solve_gen)
            except StopIteration as e:
                path = e.value
            
            end_time = time.perf_counter_ns()
            
            duration_ms = (end_time - start_time) / 1_000_000
            path_len = len(path)
            
            # Count how many cells were visited by solver
            visited_count = sum(1 for col in grid.cells for cell in col if cell.visited_by_solver)
            
            results.append({
                "iteration": i,
                "algorithm": name,
                "time_ms": duration_ms,
                "path_len": path_len,
                "visited_count": visited_count
            })
            
    # Save to CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["iteration", "algorithm", "time_ms", "path_len", "visited_count"])
        writer.writeheader()
        writer.writerows(results)
    
    print("Benchmarking complete. Results saved to results.csv")

if __name__ == "__main__":
    run_benchmark(50, 50, 1000)
