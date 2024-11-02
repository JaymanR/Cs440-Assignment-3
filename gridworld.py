import random

class GridWorld:
    def __init__(self):
        self.grid = [['-' for _ in range(13)] for _ in range(13)]
        for i in range(5, 8):
            self.grid[i][5] = 'O'
            self.grid[i][7] = 'O'
        self.grid[7][6] = 'O'
        self.bull_pos = (0, 0)
        self.robot_pos = (12, 12)
        self.target_pos = (13//2, 13//2)
        self.grid[self.target_pos[0]][self.target_pos[1]] = 'X'

    def display_grid(self):
        grid_copy = [row[:] for row in self.grid]
        bx, by = self.bull_pos
        rx, ry = self.robot_pos
        grid_copy[bx][by] = 'B'
        grid_copy[rx][ry] = 'R'
        
        for row in grid_copy:
            print(' '.join(row))
        print('\n')

    def move_robot(self, direction):
        directions = {
            'up': (-1, 0), 'down': (1, 0),
            'left': (0, -1), 'right': (0, 1),
            'up-left': (-1, -1), 'up-right': (-1, 1),
            'down-left': (1, -1), 'down-right': (1, 1)
        }
        x, y = directions.get(direction, (0, 0))
        new_pos = (self.robot_pos[0] + x, self.robot_pos[1] + y)

        if (0 <= new_pos[0] < 13 and 0 <= new_pos[1] < 13
                and self.grid[new_pos[0]][new_pos[1]] != 'O'
                and new_pos != self.bull_pos):
            self.robot_pos = new_pos

    def move_bull(self):
        bx, by = self.bull_pos
        rx, ry = self.robot_pos

        if abs(bx - rx) <= 2 and abs(by - ry) <= 2:
            possible_moves = [(bx + x, by + y) for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            possible_moves = [
                move for move in possible_moves
                if 0 <= move[0] < 13 and 0 <= move[1] < 13
                and move != self.robot_pos and self.grid[move[0]][move[1]] != 'O'
            ]
            self.bull_pos = min(possible_moves, key=lambda pos: abs(pos[0] - rx) + abs(pos[1] - ry), default=self.bull_pos)
        else:
            possible_moves = [(bx + x, by + y) for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            possible_moves = [
                move for move in possible_moves
                if 0 <= move[0] < 13 and 0 <= move[1] < 13
                and move != self.robot_pos and self.grid[move[0]][move[1]] != 'O'
            ]
            if possible_moves:
                self.bull_pos = random.choice(possible_moves)

    def is_game_over(self):
        return self.bull_pos == self.target_pos
    
    def play_round(self, robot_direction):
        self.move_robot(robot_direction)
        self.move_bull()
        self.display_grid()
        if self.is_game_over():
            print('The bull reached the target square.')
            return True
        return False
    
grid_world = GridWorld()
grid_world.display_grid()

while True:
    direction = input('Robot moves: (up, down, left, right, up-left, up-right, down-left, down-right): ')
    if direction not in ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']:
        print('Invalid direction.')
        continue
    
    game_over = grid_world.play_round(direction)
    if game_over:
        break
