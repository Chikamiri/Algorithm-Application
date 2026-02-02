from typing import Generator, List
from ..interfaces import ISolver
from ..grid import Grid
from ..cell import Cell

class WallFollower(ISolver):
    """
    Implements the 'Right-Hand Rule' wall follower algorithm.
    This is a local navigation algorithm that doesn't maintain a global frontier.
    Note: Can fail in mazes with 'islands' if the goal is inside one.
    """
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell, visualize: bool = True) -> Generator[int, None, dict]:
        # Directions: 0: Top, 1: Right, 2: Bottom, 3: Left
        direction = 1 # Initial direction: Right
        current = start_cell
        
        # path_stack will store the current solution path (pruned of loops)
        path_stack = [current]
        
        visited_count = 0
        max_frontier = 1
        
        if visualize:
            current.visited_by_solver = True
            current.is_path = True
        
        # Directions mapping: (dx, dy)
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        wall_names = ['top', 'right', 'bottom', 'left']

        while current != end_cell:
            max_frontier = max(max_frontier, len(path_stack))
            moved = False
            # Right-hand rule priority: Right, Straight, Left, Back
            for rotation in [1, 0, -1, 2]:
                new_dir = (direction + rotation) % 4
                
                if not current.walls[wall_names[new_dir]]:
                    dx, dy = moves[new_dir]
                    next_cell = grid.get_cell(current.x + dx, current.y + dy)
                    
                    if next_cell:
                        current = next_cell
                        direction = new_dir
                        visited_count += 1
                        
                        if visualize:
                            current.visited_by_solver = True
                        
                        # Loop detection for the solution path
                        if current in path_stack:
                            while path_stack[-1] != current:
                                popped = path_stack.pop()
                                if visualize:
                                    popped.is_path = False
                        else:
                            path_stack.append(current)
                            if visualize:
                                current.is_path = True
                        
                        moved = True
                        break
            
            if not moved:
                break
                
            if visualize:
                yield len(path_stack)
            
        return {
            "path": path_stack,
            "visited_count": visited_count,
            "peak_frontier": max_frontier
        }
