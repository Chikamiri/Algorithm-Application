import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import numpy as np

def analyze():
    # Structure: data[algorithm][size]['time_ms'] = [list of values]
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    try:
        with open("results.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                algo = row["algorithm"]
                size = int(row["size"])
                data[algo][size]["time_ms"].append(float(row["time_ms"]))
                data[algo][size]["path_len"].append(float(row["path_len"]))
                data[algo][size]["visited_count"].append(float(row["visited_count"]))
    except FileNotFoundError:
        print("results.csv not found. Run benchmark_runner.py first.")
        return

    algos = sorted(list(data.keys()))
    sizes = sorted(list(data[algos[0]].keys()))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    colors = plt.cm.tab10(np.linspace(0, 1, len(algos)))

    for i, algo in enumerate(algos):
        avg_times = [np.mean(data[algo][s]["time_ms"]) for s in sizes]
        avg_visited = [np.mean(data[algo][s]["visited_count"]) for s in sizes]
        avg_paths = [np.mean(data[algo][s]["path_len"]) for s in sizes]

        ax1.plot(sizes, avg_times, marker='o', label=algo, color=colors[i])
        ax2.plot(sizes, avg_visited, marker='o', label=algo, color=colors[i])
        ax3.plot(sizes, avg_paths, marker='o', label=algo, color=colors[i])

    ax1.set_title("Execution Time vs Grid Size")
    ax1.set_xlabel("Grid Size (NxN)")
    ax1.set_ylabel("Average Time (ms)")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)

    ax2.set_title("Nodes Visited vs Grid Size")
    ax2.set_xlabel("Grid Size (NxN)")
    ax2.set_ylabel("Average Nodes Visited")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    ax3.set_title("Path Length vs Grid Size")
    ax3.set_xlabel("Grid Size (NxN)")
    ax3.set_ylabel("Average Path Length")
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig("benchmark_analysis.png")
    print("Scalability Analysis complete. Plot saved as benchmark_analysis.png")

if __name__ == "__main__":
    analyze()