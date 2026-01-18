import matplotlib.pyplot as plt
import csv
from collections import defaultdict

def analyze():
    data = defaultdict(lambda: defaultdict(list))
    
    try:
        with open("results.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                algo = row["algorithm"]
                data[algo]["time_ms"].append(float(row["time_ms"]))
                data[algo]["path_len"].append(float(row["path_len"]))
                data[algo]["visited_count"].append(float(row["visited_count"]))
    except FileNotFoundError:
        print("results.csv not found. Run benchmark_runner.py first.")
        return

    algos = list(data.keys())
    avg_time = [sum(data[a]["time_ms"]) / len(data[a]["time_ms"]) for a in algos]
    avg_visited = [sum(data[a]["visited_count"]) / len(data[a]["visited_count"]) for a in algos]
    avg_path = [sum(data[a]["path_len"]) / len(data[a]["path_len"]) for a in algos]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.bar(algos, avg_time, color=['blue', 'green', 'orange'])
    ax1.set_title("Average Execution Time (ms)")
    ax1.set_ylabel("Time (ms)")

    ax2.bar(algos, avg_visited, color=['blue', 'green', 'orange'])
    ax2.set_title("Average Nodes Visited")
    ax2.set_ylabel("Count")

    ax3.bar(algos, avg_path, color=['blue', 'green', 'orange'])
    ax3.set_title("Average Path Length")
    ax3.set_ylabel("Steps")

    plt.tight_layout()
    plt.savefig("benchmark_analysis.png")
    print("Analysis complete. Plot saved as benchmark_analysis.png")
    # plt.show() # Can't show in CLI easily

if __name__ == "__main__":
    analyze()
