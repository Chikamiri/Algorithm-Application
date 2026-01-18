import heapq
from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class AStar(ISolver):
    def heuristic(self, a: Cell, b: Cell) -> int:
        """Manhattan distance heuristic."""
        return abs(a.x - b.x) + abs(a.y - b.y)

    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell) -> Generator[None, None, List[Cell]]:
        # Priority queue stores (priority, count, cell)
        # count is used to break ties and ensure stable behavior
        count = 0
        frontier = [(0, count, start_cell)]
        came_from = {start_cell: None}
        g_score = {start_cell: 0}
        
        start_cell.in_frontier = True
        
        while frontier:
            _, _, current = heapq.heappop(frontier)
            current.in_frontier = False
            current.visited_by_solver = True
            
            if current == end_cell:
                break
                
            for neighbor in grid.get_accessible_neighbors(current):
                new_g_score = g_score[current] + 1
                
                if neighbor not in g_score or new_g_score < g_score[neighbor]:
                    g_score[neighbor] = new_g_score
                    priority = new_g_score + self.heuristic(neighbor, end_cell)
                    count += 1
                    heapq.heappush(frontier, (priority, count, neighbor))
                    came_from[neighbor] = current
                    neighbor.in_frontier = True
            
            yield # Update visualization
            
        # Reconstruct path
        path = []
        if end_cell in came_from:
            temp = end_cell
            while temp:
                path.append(temp)
                temp.is_path = True
                temp = came_from[temp]
            path.reverse()
            
        return path
