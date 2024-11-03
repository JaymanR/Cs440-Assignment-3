import numpy as np
import random

GRID_SIZE = 5
TARGET = (2, 2)  # Center of the grid
BULL_START = (0, 0)  # Starting position of the bull
MOVES = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}  # Up, Down, Left, Right

# Initialize T* grid to infinity, except for the target
T_star = np.full((GRID_SIZE, GRID_SIZE), np.inf)
T_star[TARGET] = 0

# Function to check if a position is within bounds
def in_bounds(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

# Function to calculate T* values with robot influence
def update_T_star(robot_pos):
    tolerance = 1e-4
    max_iterations = 100  # Increase max iterations for proper propagation
    iteration = 0

    while iteration < max_iterations:
        max_change = 0
        new_T_star = T_star.copy()

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) == TARGET:
                    continue

                # Calculate T* based on the minimum value of neighbors
                neighbor_values = []
                for dx, dy in MOVES.values():
                    nx, ny = x + dx, y + dy
                    if in_bounds(nx, ny):
                        neighbor_values.append(T_star[nx, ny])

                # Update T*(x, y) only if there are finite neighboring values
                if neighbor_values and any(np.isfinite(val) for val in neighbor_values):
                    min_neighbor_value = min(val for val in neighbor_values if np.isfinite(val))
                    new_T_value = 1 + min_neighbor_value
                    max_change = max(max_change, abs(T_star[x, y] - new_T_value))
                    new_T_star[x, y] = new_T_value

        T_star[:, :] = new_T_star
        iteration += 1
        if max_change < tolerance:
            break

# Function to print the grid
def print_grid(bull_pos, robot_pos):
    print("\nGrid (B = Bull, R = Robot, X = Target):")
    for i in range(GRID_SIZE):
        row = ""
        for j in range(GRID_SIZE):
            if (i, j) == bull_pos:
                row += " B "
            elif (i, j) == robot_pos:
                row += " R "
            elif (i, j) == TARGET:
                row += " X "
            else:
                t_value = T_star[i, j]
                row += f"{int(t_value):2d} " if np.isfinite(t_value) else " . "
        print(row)
    print("\n" + "="*20)

# Main function
def main():
    bull_pos = BULL_START
    robot_pos = (4, 4)
    update_T_star(robot_pos)  # Initialize T* values based on robot's starting position

    while True:
        print_grid(bull_pos, robot_pos)
        print("Move the robot: (w = up, s = down, a = left, d = right, q = quit)")
        move = input("Your move: ").strip().lower()

        if move == 'q':
            print("Exiting.")
            break

        # Move the robot
        if move in MOVES:
            dx, dy = MOVES[move]
            new_robot_pos = (robot_pos[0] + dx, robot_pos[1] + dy)
            if in_bounds(*new_robot_pos):
                robot_pos = new_robot_pos
                update_T_star(robot_pos)
            else:
                print("Move is out of bounds.")
        else:
            print("Invalid move. Use 'w', 's', 'a', 'd' to move, 'q' to quit.")

        # Move the bull probabilistically
        possible_moves = []
        for dx, dy in MOVES.values():
            new_bull_pos = (bull_pos[0] + dx, bull_pos[1] + dy)
            if in_bounds(*new_bull_pos):
                # Higher probability to move toward robot if within influence range
                if abs(bull_pos[0] - robot_pos[0]) <= 2 and abs(bull_pos[1] - robot_pos[1]) <= 2:
                    prob = 0.75 if abs(new_bull_pos[0] - robot_pos[0]) + abs(new_bull_pos[1] - robot_pos[1]) < abs(bull_pos[0] - robot_pos[0]) + abs(bull_pos[1] - robot_pos[1]) else 0.25
                else:
                    prob = 0.25
                possible_moves.append((prob, new_bull_pos))

        # Select the bull's move based on probabilities
        move_probs, move_positions = zip(*possible_moves)
        bull_pos = random.choices(move_positions, weights=move_probs)[0]

        # Check if bull has reached the target
        if bull_pos == TARGET:
            print_grid(bull_pos, robot_pos)
            print("The bull has reached the target!")
            break

main()
