import time
import csv
import sys
import os
import psutil
from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar
from model.solvers.dijkstra import Dijkstra
from model.solvers.wall_follower import WallFollower

from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.generators.prims import PrimsAlgorithm
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar
from model.solvers.dijkstra import Dijkstra
from model.solvers.wall_follower import WallFollower

def run_benchmark(sizes=[10, 20, 30, 40, 50, 75, 100], iterations=20):
    solvers = {
        "BFS": BFS(),
        "DFS": DFS(),
        "AStar": AStar(),
        "Dijkstra": Dijkstra(),
        "WallFollower": WallFollower()
    }
    
    generators = {
        "RecursiveBacktracker": RecursiveBacktracker(),
        "Prims": PrimsAlgorithm()
    }
    
    results = []
    process = psutil.Process(os.getpid())
    
    print(f"Starting Scalability Benchmark...")
    
    for gen_name, generator in generators.items():
        print(f"--- Testing Generator: {gen_name} ---")
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
                    
                    # Run WITHOUT visualization for max speed and accurate timing
                    solve_gen = solver.solve(grid, start_cell, end_cell, visualize=False)
                    try:
                        while True:
                            next(solve_gen)
                    except StopIteration as e:
                        results_dict = e.value
                    
                    end_time = time.perf_counter_ns()
                    duration_ms = (end_time - start_time) / 1_000_000
                    mem_kb = process.memory_info().rss / 1024
                    
                    results.append({
                        "generator": gen_name,
                        "size": size,
                        "iteration": i,
                        "algorithm": name,
                        "time_ms": duration_ms,
                        "path_len": len(results_dict["path"]),
                        "visited_count": results_dict["visited_count"],
                        "peak_frontier": results_dict["peak_frontier"],
                        "memory_kb": mem_kb
                    })
            
    # Save to CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["generator", "size", "iteration", "algorithm", "time_ms", "path_len", "visited_count", "peak_frontier", "memory_kb"])
        writer.writeheader()
        writer.writerows(results)
    
    print("Benchmarking complete. Results saved to results.csv")

if __name__ == "__main__":

    # Increased recursion limit for deep mazes

    sys.setrecursionlimit(10**7)

    

    # Testing sizes as requested

    run_benchmark(sizes=[10, 50, 100, 200, 300], iterations=2)






