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
    def solve(self, grid: Grid, start_cell: Cell, end_cell: Cell) -> Generator[None, None, List[Cell]]:
        # Directions: 0: Top, 1: Right, 2: Bottom, 3: Left
        # We start by facing 'Right' or 'Down' depending on start position
        direction = 1 # Initial direction: Right
        current = start_cell
        
        path = [current]
        current.visited_by_solver = True
        current.is_path = True
        
        # Directions mapping: (dx, dy)
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        wall_names = ['top', 'right', 'bottom', 'left']

        while current != end_cell:
            # Right-hand rule priority:
            # 1. Turn Right (relative to current direction)
            # 2. Go Straight
            # 3. Turn Left
            # 4. Turn Back
            
            moved = False
            # Check relative directions: Right (dir+1), Straight (dir), Left (dir-1), Back (dir+2)
            for rotation in [1, 0, -1, 2]:
                new_dir = (direction + rotation) % 4
                
                # Check if there is a wall in that direction
                if not current.walls[wall_names[new_dir]]:
                    dx, dy = moves[new_dir]
                    next_cell = grid.get_cell(current.x + dx, current.y + dy)
                    
                    if next_cell:
                        current = next_cell
                        direction = new_dir
                        
                        # In wall follower, we might visit the same cell multiple times
                        # But for consistency with other solvers, we mark it.
                        # Note: 'is_path' for wall follower is tricky because it's the actual walk.
                        current.visited_by_solver = True
                        path.append(current)
                        
                        # For visualization, we'll mark all cells currently in our "path"
                        # Since wall follower can backtrack, this will show the "string" behind it.
                        current.is_path = True
                        
                        moved = True
                        break
            
            if not moved:
                # This should logically not happen in a valid maze
                break
                
            yield # Update visualization
            
        return path
