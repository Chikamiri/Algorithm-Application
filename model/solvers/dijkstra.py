import heapq
from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class Dijkstra(ISolver):
    """
    Implements Dijkstra's algorithm. 
    In an unweighted grid, this behaves like BFS but uses a priority queue.
    Useful for comparison with A*.
    """
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell, visualize: bool = True) -> Generator[int, None, dict]:
        # Priority Queue: (distance, (x, y))
        pq = [(0, (start_cell.x, start_cell.y))]
        distances = {(start_cell.x, start_cell.y): 0}
        came_from = {start_cell: None}
        
        visited_count = 0
        max_frontier = 1
        
        if visualize:
            start_cell.in_frontier = True
        
        while pq:
            max_frontier = max(max_frontier, len(pq))
            dist, (curr_x, curr_y) = heapq.heappop(pq)
            current = grid.get_cell(curr_x, curr_y)
            
            if not current: continue
            
            visited_count += 1
            if visualize:
                current.in_frontier = False
                current.visited_by_solver = True
            
            if current == end_cell:
                break
                
            for neighbor in grid.get_accessible_neighbors(current):
                new_dist = dist + 1
                neighbor_coords = (neighbor.x, neighbor.y)
                
                if neighbor_coords not in distances or new_dist < distances[neighbor_coords]:
                    distances[neighbor_coords] = new_dist
                    came_from[neighbor] = current
                    if visualize:
                        neighbor.in_frontier = True
                    heapq.heappush(pq, (new_dist, neighbor_coords))
            
            if visualize:
                yield len(pq)
            
        # Reconstruct path
        path = []
        if end_cell in came_from:
            temp = end_cell
            while temp:
                path.append(temp)
                if visualize:
                    temp.is_path = True
                temp = came_from[temp]
            path.reverse()
        
        return {
            "path": path,
            "visited_count": visited_count,
            "peak_frontier": max_frontier
        }
