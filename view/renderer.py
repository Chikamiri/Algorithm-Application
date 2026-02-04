import pygame
from model.grid import Grid
from model.cell import Cell

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.SIDEBAR_WIDTH = 300
        
        # Modern Color Palette (Nord-like)
        self.COLOR_BG = (46, 52, 64)       # Polar Night
        self.COLOR_WALL = (216, 222, 233)  # Snow Storm
        self.COLOR_SIDEBAR_BG = (40, 44, 52) # Darker BG for Sidebar
        
        # Generator colors
        self.COLOR_VISITED_GEN = (59, 66, 82) # Darker Polar Night for visited
        self.COLOR_CURRENT = (208, 135, 112)  # Aurora Orange (distinct from Start)
        
        # Solver colors
        self.COLOR_FRONTIER = (136, 192, 208) # Frost Cyan
        self.COLOR_VISITED_SOLVE = (94, 129, 172) # Frost Blue
        self.COLOR_PATH = (235, 203, 139)     # Aurora Yellow
        
        self.COLOR_ENTRY = (191, 97, 106)    # Aurora Red (Start)
        self.COLOR_EXIT = (163, 190, 140)     # Aurora Green (End)
        self.COLOR_TEXT = (236, 239, 244)     # Snow Storm Light
        
        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', 16)
        self.font_large = pygame.font.SysFont('Consolas', 24, bold=True)

        # Dynamic Metrics (Calculated per frame)
        self.cell_size = 20
        self.offset_x = 10
        self.offset_y = 10

    def calculate_metrics(self, grid: Grid):
        # Calculate available space for maze
        available_w = self.screen.get_width() - self.SIDEBAR_WIDTH - 20 # 20 padding
        available_h = self.screen.get_height() - 20 # 20 padding
        
        # Determine cell size to fit
        cell_w = available_w // grid.cols
        cell_h = available_h // grid.rows
        self.cell_size = max(4, min(cell_w, cell_h)) # Minimum 4px size
        
        # Center the maze in the available area
        maze_w = self.cell_size * grid.cols
        maze_h = self.cell_size * grid.rows
        
        self.offset_x = 10 + (available_w - maze_w) // 2
        self.offset_y = 10 + (available_h - maze_h) // 2

    def draw_grid(self, grid: Grid):
        self.screen.fill(self.COLOR_BG)
        
        # Draw Sidebar Background
        sidebar_rect = pygame.Rect(self.screen.get_width() - self.SIDEBAR_WIDTH, 0, self.SIDEBAR_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, self.COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(self.screen, self.COLOR_WALL, (sidebar_rect.x, 0), (sidebar_rect.x, self.screen.get_height()), 2)
        
        self.calculate_metrics(grid)
        
        # First pass: Draw cell backgrounds (visited states)
        for col in grid.cells:
            for cell in col:
                self.draw_cell_background(cell)

        # Second pass: Draw walls
        for col in grid.cells:
            for cell in col:
                self.draw_cell_walls(cell)
                
        # Third pass: Draw Path overlays
        for col in grid.cells:
            for cell in col:
                if cell.is_path:
                    self.draw_path_connection(cell, grid)

    def draw_cell_background(self, cell: Cell):
        x = cell.x * self.cell_size + self.offset_x
        y = cell.y * self.cell_size + self.offset_y
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        # Priority 1: Entry/Exit (Fill whole cell)
        if cell.is_entry:
            pygame.draw.rect(self.screen, self.COLOR_ENTRY, rect)
        elif cell.is_exit:
            pygame.draw.rect(self.screen, self.COLOR_EXIT, rect)
        # Priority 2: Solver states
        elif cell.in_frontier:
            pygame.draw.rect(self.screen, self.COLOR_FRONTIER, rect)
        elif cell.visited_by_solver:
            pygame.draw.rect(self.screen, self.COLOR_VISITED_SOLVE, rect)
        # Priority 3: Generator visited
        elif cell.visited:
            pygame.draw.rect(self.screen, self.COLOR_VISITED_GEN, rect)

    def draw_path_connection(self, cell: Cell, grid: Grid):
        cx = cell.x * self.cell_size + self.offset_x + self.cell_size // 2
        cy = cell.y * self.cell_size + self.offset_y + self.cell_size // 2
        
        neighbors = grid.get_accessible_neighbors(cell)
        for n in neighbors:
            if n.is_path:
                nx = n.x * self.cell_size + self.offset_x + self.cell_size // 2
                ny = n.y * self.cell_size + self.offset_y + self.cell_size // 2
                pygame.draw.line(self.screen, self.COLOR_PATH, (cx, cy), (nx, ny), max(2, self.cell_size // 3))

    def draw_cell_walls(self, cell: Cell):
        x = cell.x * self.cell_size + self.offset_x
        y = cell.y * self.cell_size + self.offset_y
        
        wall_color = self.COLOR_WALL
        width = max(1, int(self.cell_size * 0.1)) # Dynamic wall width
        
        if cell.walls['top']:
            pygame.draw.line(self.screen, wall_color, (x, y), (x + self.cell_size, y), width)
        if cell.walls['right']:
            pygame.draw.line(self.screen, wall_color, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), width)
        if cell.walls['bottom']:
            pygame.draw.line(self.screen, wall_color, (x + self.cell_size, y + self.cell_size), (x, y + self.cell_size), width)
        if cell.walls['left']:
            pygame.draw.line(self.screen, wall_color, (x, y + self.cell_size), (x, y), width)

    def draw_current(self, cell: Cell):
        if not cell:
            return
        x = cell.x * self.cell_size + self.offset_x
        y = cell.y * self.cell_size + self.offset_y
        
        # Smaller pointer
        inset = self.cell_size // 4
        size = self.cell_size - (inset * 2)
        rect = pygame.Rect(x + inset, y + inset, size, size)
        pygame.draw.rect(self.screen, self.COLOR_CURRENT, rect, border_radius=max(2, self.cell_size // 8))

    def draw_pause_overlay(self):
        # Draw over the maze area only? Or whole screen? Let's do maze area
        area_w = self.screen.get_width() - self.SIDEBAR_WIDTH
        s = pygame.Surface((area_w, self.screen.get_height()))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        text = self.font_large.render("PAUSED", True, self.COLOR_TEXT)
        text_rect = text.get_rect(center=(area_w // 2, self.screen.get_height() // 2))
        
        box_rect = text_rect.inflate(40, 40)
        pygame.draw.rect(self.screen, self.COLOR_BG, box_rect)
        pygame.draw.rect(self.screen, self.COLOR_WALL, box_rect, 2)
        
        self.screen.blit(text, text_rect)

    def draw_info(self, algo_name, speed_info, grid_size, stats=None):
        x_start = self.screen.get_width() - self.SIDEBAR_WIDTH + 20
        y_start = 20
        
        # Title
        title = self.font_large.render("Maze Visualizer", True, self.COLOR_PATH)
        self.screen.blit(title, (x_start, y_start))
        y_start += 50
        
        # --- Live Statistics Panel ---
        # Draw a background box for stats to make it distinct
        stats_h = 200 # Increased height for even more stats
        stats_w = self.SIDEBAR_WIDTH - 40
        stats_rect = pygame.Rect(x_start, y_start, stats_w, stats_h)
        pygame.draw.rect(self.screen, (35, 39, 46), stats_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLOR_FRONTIER, stats_rect, 2, border_radius=8)
        
        # Stats Data
        visited_txt = f"{stats['visited']}" if stats else "0"
        total_txt = f"{stats['total']}" if stats else "0"
        coverage_txt = f"{stats['coverage']:.1f}%" if stats else "0.0%"
        frontier_txt = f"{stats['frontier']}" if stats else "0"
        path_txt = f"{stats['path']}" if stats else "0"
        time_txt = f"{stats['time']:.2f}s" if stats and 'time' in stats else "0.00s"
        comp_txt = f"{stats['comp_time']:.2f}ms" if stats and 'comp_time' in stats else "0.00ms"
        steps_txt = f"{stats['steps']}" if stats and 'steps' in stats else "0"
        ram_txt = f"{stats['memory']:.1f} KB" if stats and 'memory' in stats else "0.0 KB"
        
        stat_lines = [
            f"Visual Time:    {time_txt}",
            f"Execution Time: {comp_txt}",
            f"Total Steps:    {steps_txt}",
            f"RAM Usage:      {ram_txt}",
            f"Nodes Visited:  {visited_txt}",
            f"Total Cells:    {total_txt}",
            f"Coverage:       {coverage_txt}",
            f"Frontier Size:  {frontier_txt}",
            f"Path Length:    {path_txt}"
        ]
        
        sy = y_start + 15 # Adjusted padding
        for line in stat_lines:
            t = self.font.render(line, True, self.COLOR_TEXT)
            self.screen.blit(t, (x_start + 15, sy))
            sy += 22
            
        y_start += stats_h + 20 # Move below stats box
        
        # --- Other Info Groups ---
        info_groups = [
            ("Status", [
                f"Algorithm: {algo_name}",
                f"Grid Size: {grid_size[0]}x{grid_size[1]}",
                f"Speed: {speed_info}",
            ]),
            ("Controls", [
                "SPACE: Pause / Resume",
                "R: Reset Grid",
                "B: Benchmark Mode",
                "[ / ]: Speed +/- 1",
                "Shift+[ / ]: Speed +/- 5",
            ]),
            ("Grid Sizing", [
                "ARROWS: Resize (+/- 5)",
                "F1: Small (15x15)",
                "F2: Medium (30x40)",
                "F3: Large (50x70)",
            ]),
            ("Algorithms", [
                "1: Rec. Backtracker",
                "2: Prim's Algo",
                "---",
                "3: BFS (Shortest)",
                "4: DFS",
                "5: A* (Heuristic)",
                "6: Dijkstra",
                "7: Wall Follower",
            ])
        ]
        
        for group_title, lines in info_groups:
            # Group Header
            head = self.font.render(group_title, True, self.COLOR_FRONTIER)
            self.screen.blit(head, (x_start, y_start))
            y_start += 25
            
            # Lines
            for line in lines:
                text = self.font.render(line, True, self.COLOR_TEXT)
                self.screen.blit(text, (x_start + 10, y_start))
                y_start += 20
            
            y_start += 15 # Group spacing

    def draw_benchmark_progress(self, progress, message, current_ram=0.0):
        self.screen.fill(self.COLOR_BG)
        
        # ... (keep sidebar logic) ...
        sidebar_rect = pygame.Rect(self.screen.get_width() - self.SIDEBAR_WIDTH, 0, self.SIDEBAR_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, self.COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(self.screen, self.COLOR_WALL, (sidebar_rect.x, 0), (sidebar_rect.x, self.screen.get_height()), 2)
        
        # Center Area
        area_w = self.screen.get_width() - self.SIDEBAR_WIDTH
        center_x = area_w // 2
        center_y = self.screen.get_height() // 2
        
        # Title
        title = self.font_large.render("Running Benchmarks...", True, self.COLOR_PATH)
        title_rect = title.get_rect(center=(center_x, center_y - 80))
        self.screen.blit(title, title_rect)
        
        # RAM Usage Real-time
        ram_text = self.font_large.render(f"Live RAM: {current_ram:.1f} KB", True, self.COLOR_FRONTIER)
        ram_rect = ram_text.get_rect(center=(center_x, center_y - 30))
        self.screen.blit(ram_text, ram_rect)

        # Progress Bar
        bar_w = 400
        bar_h = 30
        pygame.draw.rect(self.screen, self.COLOR_VISITED_GEN, (center_x - bar_w // 2, center_y + 20, bar_w, bar_h))
        pygame.draw.rect(self.screen, self.COLOR_ENTRY, (center_x - bar_w // 2, center_y + 20, int(bar_w * progress), bar_h))
        pygame.draw.rect(self.screen, self.COLOR_WALL, (center_x - bar_w // 2, center_y + 20, bar_w, bar_h), 2)
        
        # Message
        msg_surf = self.font.render(message, True, self.COLOR_TEXT)
        msg_rect = msg_surf.get_rect(center=(center_x, center_y + 70))
        self.screen.blit(msg_surf, msg_rect)

    def draw_benchmark_results(self, stats, iterations=5):
        self.screen.fill(self.COLOR_BG)
        
        # Draw Sidebar Background
        sidebar_rect = pygame.Rect(self.screen.get_width() - self.SIDEBAR_WIDTH, 0, self.SIDEBAR_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, self.COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(self.screen, self.COLOR_WALL, (sidebar_rect.x, 0), (sidebar_rect.x, self.screen.get_height()), 2)
        
        # Instructions
        info_x = self.screen.get_width() - self.SIDEBAR_WIDTH + 20
        self.screen.blit(self.font_large.render("Benchmark Results", True, self.COLOR_PATH), (info_x, 20))
        self.screen.blit(self.font.render("Press B to return", True, self.COLOR_TEXT), (info_x, 60))
        self.screen.blit(self.font.render("Press ENTER to rerun", True, self.COLOR_TEXT), (info_x, 90))
        
        # Iteration Control
        iter_y = 130
        self.screen.blit(self.font.render(f"Target Iterations: {iterations}", True, self.COLOR_FRONTIER), (info_x, iter_y))
        self.screen.blit(self.font.render("(UP/DOWN +/- 1, SHIFT +/- 5)", True, (150, 150, 150)), (info_x, iter_y + 20))

        if not stats:
            # Draw "No Results" message in center
            area_w = self.screen.get_width() - self.SIDEBAR_WIDTH
            msg = self.font_large.render("No results available. Press ENTER to start.", True, self.COLOR_TEXT)
            msg_rect = msg.get_rect(center=(area_w // 2, self.screen.get_height() // 2))
            self.screen.blit(msg, msg_rect)
            return

        # Detailed Stats Table in Sidebar
        ty = 180
        for name, data in stats.items():
            head = self.font.render(f"--- {name} ---", True, self.COLOR_FRONTIER)
            self.screen.blit(head, (info_x, ty))
            ty += 22
            
            detail_lines = [
                f"Time: {data['time_min']:.1f} - {data['time_max']:.1f} ms",
                f"RAM: {data['memory_avg']:.1f} KB (Peak: {data['memory_max']:.1f})",
                f"Efficiency: {data['efficiency']:.1f} nodes/ms",
                f"Peak Frontier: {data['frontier_max']}",
                f"Visited Range: {data['visited_min']} - {data['visited_max']}",
            ]
            for line in detail_lines:
                txt = self.font.render(line, True, self.COLOR_TEXT)
                self.screen.blit(txt, (info_x + 10, ty))
                ty += 18
            ty += 10

        # Draw Charts
        area_w = self.screen.get_width() - self.SIDEBAR_WIDTH
        padding = 40
        chart_w = (area_w - padding * 3) // 3
        chart_h = self.screen.get_height() - 200
        y_start = 100
        
        algos = list(stats.keys())
        colors = [
            self.COLOR_FRONTIER, 
            self.COLOR_EXIT, 
            self.COLOR_PATH, 
            self.COLOR_CURRENT, 
            self.COLOR_ENTRY
        ]
        
        # 1. Time Chart
        times = [stats[a]['time_avg'] for a in algos]
        self.draw_bar_chart(padding, y_start, chart_w, chart_h, algos, times, "Avg Time (ms)", colors)
        
        # 2. Visited Chart
        visited = [stats[a]['visited_avg'] for a in algos]
        self.draw_bar_chart(padding * 2 + chart_w, y_start, chart_w, chart_h, algos, visited, "Avg Visited", colors)
        
        # 3. Path Len Chart
        paths = [stats[a]['path_avg'] for a in algos]
        self.draw_bar_chart(padding * 3 + chart_w * 2, y_start, chart_w, chart_h, algos, paths, "Avg Path", colors)

        # 4. Memory Chart
        mems = [stats[a]['memory_avg'] for a in algos]
        self.draw_bar_chart(padding * 4 + chart_w * 3, y_start, chart_w, chart_h, algos, mems, "Avg RAM (KB)", colors)

    def draw_bar_chart(self, x, y, w, h, labels, values, title, colors):
        # Title
        title_surf = self.font.render(title, True, self.COLOR_TEXT)
        self.screen.blit(title_surf, (x + w//2 - title_surf.get_width()//2, y - 30))
        
        # Axes
        pygame.draw.line(self.screen, self.COLOR_WALL, (x, y + h), (x + w, y + h), 2) # X
        pygame.draw.line(self.screen, self.COLOR_WALL, (x, y), (x, y + h), 2) # Y
        
        if not values: return
        max_val = max(values) if max(values) > 0 else 1
        
        # Grid lines (5 lines)
        for i in range(1, 6):
            gy = y + h - (i * h / 5)
            pygame.draw.line(self.screen, (60, 60, 60), (x, gy), (x + w, gy), 1)
            # Label
            val = (max_val / 5) * i
            lbl = self.font.render(f"{val:.0f}", True, (100, 100, 100))
            self.screen.blit(lbl, (x - lbl.get_width() - 5, gy - 10))
        
        bar_width = w // len(values) - 10
        
        for i, val in enumerate(values):
            bar_h = int((val / max_val) * (h - 20))
            bx = x + i * (bar_width + 10) + 5
            by = y + h - bar_h
            
            # Bar
            color = colors[i % len(colors)]
            pygame.draw.rect(self.screen, color, (bx, by, bar_width, bar_h))
            
            # Value Label
            val_text = f"{val:.1f}"
            val_surf = self.font.render(val_text, True, self.COLOR_TEXT)
            self.screen.blit(val_surf, (bx + bar_width//2 - val_surf.get_width()//2, by - 20))
            
            # X Label
            lbl_surf = self.font.render(labels[i], True, self.COLOR_TEXT)
            self.screen.blit(lbl_surf, (bx + bar_width//2 - lbl_surf.get_width()//2, y + h + 5))