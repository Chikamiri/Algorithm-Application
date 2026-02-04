import time
import csv
import sys
import os
import psutil
import multiprocessing
from model.grid import Grid
from model.generators.recursive_backtracker import RecursiveBacktracker
from model.generators.prims import PrimsAlgorithm
from model.solvers.bfs import BFS
from model.solvers.dfs import DFS
from model.solvers.astar import AStar
from model.solvers.dijkstra import Dijkstra
from model.solvers.wall_follower import WallFollower

# Increased recursion limit for deep mazes in all processes
sys.setrecursionlimit(10**7)

def run_single_iteration(args):
    """Worker function to run a single benchmark iteration."""
    gen_name, size, iteration = args
    
    # Instantiate generators and solvers inside the worker process
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
    
    generator = generators[gen_name]
    results = []
    process = psutil.Process(os.getpid())
    
    rows, cols = size, size
    
    # Generate a new maze for this iteration
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
            "iteration": iteration,
            "algorithm": name,
            "time_ms": duration_ms,
            "path_len": len(results_dict["path"]),
            "visited_count": results_dict["visited_count"],
            "peak_frontier": results_dict["peak_frontier"],
            "memory_kb": mem_kb
        })
    
    return results

def run_benchmark(sizes=[100, 250, 500, 750, 1000], iterations=50):
    generators = ["RecursiveBacktracker", "Prims"]
    
    tasks = []
    for gen_name in generators:
        for size in sizes:
            for i in range(iterations):
                tasks.append((gen_name, size, i))
    
    total_tasks = len(tasks)
    print(f"Starting Scalability Benchmark with {multiprocessing.cpu_count()} cores...")
    print(f"Total iterations to run: {total_tasks}")
    
    results = []
    
    # Use a Process Pool to run tasks in parallel
    with multiprocessing.Pool() as pool:
        # Use imap_unordered for slightly better performance and to show progress
        count = 0
        for task_results in pool.imap_unordered(run_single_iteration, tasks):
            results.extend(task_results)
            count += 1
            if count % 10 == 0 or count == total_tasks:
                print(f"Progress: {count}/{total_tasks} iterations complete ({(count/total_tasks)*100:.1f}%)", end='\r')
    
    print("\nBenchmarking complete. Saving results...")
    
    # Save to CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["generator", "size", "iteration", "algorithm", "time_ms", "path_len", "visited_count", "peak_frontier", "memory_kb"])
        writer.writeheader()
        writer.writerows(results)
    
    print("Results saved to results.csv")

if __name__ == "__main__":
    # Testing sizes as requested
    run_benchmark(sizes=[100, 250, 500, 750, 1000], iterations=5)
