# Project Improvement Plan: Maze Algorithm Visualizer

This document outlines strategic improvements to the Maze Algorithm Visualizer project. These enhancements are designed not just to add features, but specifically to generate high-quality data and analysis for the final project report (`report_template.pdf`).

## 1. Algorithmic Enhancements

### Add "Greedy Best-First Search"
**Current State:** The project includes Uninformed Search (BFS, DFS) and Optimal Search (A*, Dijkstra).
**Proposal:** Implement **Greedy Best-First Search**.
**Logic:** Like A*, but uses *only* the heuristic ($h(n)$) for priority, ignoring path cost ($g(n)$).
**Value for Report:**
*   **Contrast:** Provides a perfect middle-ground for comparison.
*   **Discussion Point (Section 5.5):** Allows you to discuss the trade-off between *speed* (Greedy BFS is often faster/visits fewer nodes) and *optimality* (Greedy BFS does not guarantee the shortest path).

## 2. Experimental Design Improvements

### Compare Maze "Textures" (Topology Analysis)
**Current State:** The benchmarking suite (`benchmark_runner.py`) only tests against `Recursive Backtracker` mazes.
**Proposal:** Update `benchmark_runner.py` to run all solvers against **both** `Recursive Backtracker` AND `Prim's Algorithm`.
**Value for Report:**
*   **Recursive Backtracker:** Generates "River" mazes (long, winding corridors, few dead ends). Favors DFS.
*   **Prim's Algorithm:** Generates "Classic" mazes (many short branches, many dead ends). Harder for DFS, typically easier for BFS/A*.
*   **Critical Analysis:** Proves that algorithm performance is strictly dependent on the environment topology.

### Add "Peak Memory" Metric
**Current State:** We track `visited_count` (total work/time complexity proxy).
**Proposal:** Track `max_frontier_size`. This is the maximum number of items in the priority queue or stack at any single moment.
**Value for Report:**
*   **Complexity Analysis (Section 4.3):** Empirically proves Space Complexity.
    *   **BFS:** High space complexity (frontier grows with radius).
    *   **DFS:** Low space complexity (frontier grows with depth).
    *   **A*:** Variable, often high.

## 3. Benchmarking Strategy

### Statistical Significance over Raw Scale
**Current State:** The script attempts huge grid sizes (up to 10,000x10,000) which is impractical.
**Proposal:** 
*   Cap grid size at reasonable limits (e.g., 50x50 to 200x200).
*   Increase **Iterations** (e.g., 50-100 runs per size).
*   Calculate **Standard Deviation** alongside Averages.
**Value for Report:**
*   **Scientific Rigor:** Showing error bars or standard deviation demonstrates that your results are consistent and not just luck.

## 4. Visualization Polish

### Search Heatmaps
**Proposal:** Add a mode that doesn't just show the final path, but colors cells based on "visit order" or "distance from start" using a gradient (e.g., Cold Blue $\to$ Hot Red).
**Value for Report:**
*   **Illustrations (Section 4.4):** A screenshot comparing the circular search pattern of BFS vs. the directed "beam" of A* is a powerful visual aid for explaining *how* the algorithms differ.

## 5. Mapping Improvements to Report Sections

| Improvement | Relevant Report Section | Narrative |
| :--- | :--- | :--- |
| **Greedy BFS** | **5.5 Phân tích kết quả** | "While A* guarantees the shortest path, Greedy BFS found a solution 30% faster in 80% of test cases, albeit with a 10% longer path." |
| **Maze Textures** | **5.3 Các bộ dữ liệu** | "We utilized two distinct maze topologies to stress-test the solvers: River-style (Recursive) and Branching-style (Prims)." |
| **Peak Memory** | **4.3 Độ phức tạp** | "Empirical data confirms theoretical bounds: BFS required 4x more memory (Peak Frontier) than DFS on 100x100 grids." |
| **Stats/Std Dev** | **5.2 Phương pháp so sánh** | "All results represent the average of 100 independent trials to minimize noise from random maze generation." |
