from view.view import COLORS

class Spot:
    
    TOTAL_ROWS = 71
    TOTAL_COLUMNS = 200
    

    def __init__(self, row, col, state, width, height) -> None:
        self.row = row
        self.col = col
        self.neighbors = []
        
        self.color = COLORS[state] if COLORS.get(state) != None else COLORS["checkpoint"]
        self.state = state

        self.square_height = (height // self.TOTAL_ROWS)
        self.square_width = (width // self.TOTAL_COLUMNS)

        self.x = self.col * self.square_width
        self.y = self.row * self.square_height

    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.state == '#' or self.state == 'P'
    
    def set_state(self, state):
        self.state = state


    def make_open(self):
        pass

    def make_close(self):
        pass

    def update_neighbors(self, grid):
        self.neighbors = []


        if (
            self.row < self.TOTAL_ROWS - 2 
            and not grid[self.row + 1][self.col].is_closed()
        ): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if (
            self.row > 0 
            and not grid[self.row - 1][self.col].is_closed()
        ): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if (
            self.col > 0
            and not grid[self.row][self.col - 1].is_closed()
        ): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if (
            self.col < self.TOTAL_COLUMNS - 1
            and not grid[self.row][self.col + 1].is_closed()
        ): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])


    def __str__(self) -> str:
        return f"row: {self.row}  col: {self.col}  state: {self.state}"
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
