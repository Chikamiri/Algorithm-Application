import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import numpy as np

def analyze():
    # Structure: data[generator][algorithm][size]['metric'] = [list of values]
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    
    try:
        with open("results.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                gen = row.get("generator", "RecursiveBacktracker")
                algo = row["algorithm"]
                size = int(row["size"])
                data[gen][algo][size]["time_ms"].append(float(row["time_ms"]))
                data[gen][algo][size]["path_len"].append(float(row["path_len"]))
                data[gen][algo][size]["visited_count"].append(float(row["visited_count"]))
                data[gen][algo][size]["peak_frontier"].append(float(row.get("peak_frontier", 0)))
    except FileNotFoundError:
        print("results.csv not found. Run benchmark_runner.py first.")
        return

    generators = sorted(list(data.keys()))
    
    for gen in generators:
        algos = sorted(list(data[gen].keys()))
        sizes = sorted(list(data[gen][algos[0]].keys()))

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f"Scalability Analysis: {gen} Maze", fontsize=16)
        
        ax_time, ax_visited = axes[0]
        ax_path, ax_frontier = axes[1]

        colors = plt.cm.tab10(np.linspace(0, 1, len(algos)))

        for i, algo in enumerate(algos):
            avg_times = [np.mean(data[gen][algo][s]["time_ms"]) for s in sizes]
            avg_visited = [np.mean(data[gen][algo][s]["visited_count"]) for s in sizes]
            avg_paths = [np.mean(data[gen][algo][s]["path_len"]) for s in sizes]
            avg_frontier = [np.mean(data[gen][algo][s]["peak_frontier"]) for s in sizes]

            ax_time.plot(sizes, avg_times, marker='o', label=algo, color=colors[i])
            ax_visited.plot(sizes, avg_visited, marker='o', label=algo, color=colors[i])
            ax_path.plot(sizes, avg_paths, marker='o', label=algo, color=colors[i])
            ax_frontier.plot(sizes, avg_frontier, marker='o', label=algo, color=colors[i])

        ax_time.set_title("Execution Time vs Grid Size")
        ax_time.set_ylabel("Average Time (ms)")
        ax_time.legend()
        ax_time.grid(True, linestyle='--', alpha=0.7)

        ax_visited.set_title("Nodes Expanded vs Grid Size")
        ax_visited.set_ylabel("Average Nodes Expanded")
        ax_visited.legend()
        ax_visited.grid(True, linestyle='--', alpha=0.7)

        ax_path.set_title("Path Length vs Grid Size")
        ax_path.set_ylabel("Average Path Length")
        ax_path.legend()
        ax_path.grid(True, linestyle='--', alpha=0.7)
        
        ax_frontier.set_title("Peak Frontier Size (Space Complexity)")
        ax_frontier.set_ylabel("Max Nodes in Frontier")
        ax_frontier.legend()
        ax_frontier.grid(True, linestyle='--', alpha=0.7)

        for ax in axes.flat:
            ax.set_xlabel("Grid Size (NxN)")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        filename = f"benchmark_{gen}.png"
        plt.savefig(filename)
        print(f"Analysis for {gen} complete. Plot saved as {filename}")

if __name__ == "__main__":
    analyze()

if __name__ == "__main__":
    analyze()