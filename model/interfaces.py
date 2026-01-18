from abc import ABC, abstractmethod
from typing import Generator, Any, Tuple

class IGenerator(ABC):
    """
    Interface for Maze Generation Algorithms.
    """
    @abstractmethod
    def generate(self, grid: Any) -> Generator[None, None, None]:
        """
        Generates the maze structure.
        
        Args:
            grid: The Grid object to modify.
            
        Yields:
            None: Yields control back to the caller for visualization updates.
        """
        pass

class ISolver(ABC):
    """
    Interface for Maze Solving Algorithms.
    """
    @abstractmethod
    def solve(self, grid: Any, start_cell: Any, end_cell: Any) -> Generator[None, None, list[Any]]:
        """
        Solves the maze.

        Args:
            grid: The Grid object.
            start_cell: The starting Cell.
            end_cell: The goal Cell.

        Yields:
            None: Yields control back to the caller for visualization updates.
            
        Returns:
            list[Cell]: The path from start to end.
        """
        pass
