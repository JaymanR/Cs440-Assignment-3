import numpy as np

GRID_SIZE = 13
TARGET = (6, 6)
BULL_POSITION = (0, 0)
ROBOT_POSITION = (12, 12)
OBSTACLES = {(5, 5), (5, 6), (5, 7), (6, 7), (7, 5), (7, 6), (7, 7)}

T_star = {(posB, posC): float('inf') for posB in np.ndindex(GRID_SIZE, GRID_SIZE)
          for posC in np.ndindex(GRID_SIZE, GRID_SIZE)}
for posC in np.ndindex(GRID_SIZE, GRID_SIZE):
    T_star[(TARGET, posC)] = 0

POSSIBLE_BULL_MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
POSSIBLE_ROBOT_MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

def check_bounds(pos):
    x, y = pos
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and pos not in OBSTACLES

def possible_moves(pos, moves):
    x, y = pos
    return [(x + dx, y + dy) for dx, dy in moves if check_bounds((x + dx, y + dy))]

# calculates the manhattan distance from pos1 to pos2
def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_in_bull_range(bull_pos, robot_pos):
    return calculate_distance(bull_pos, robot_pos) <= 4

# Main value iteration loop
threshold = 1e-4
converged = False
iteration = 0

while not converged:
    max_change = 0
    new_T_star = T_star.copy()

    for posB in np.ndindex(GRID_SIZE, GRID_SIZE):
        for posC in np.ndindex(GRID_SIZE, GRID_SIZE):
            if posB == TARGET:
                new_T_star[(posB, posC)] = 0
                continue

            # Calculate expected T* value for the current state
            expected_values = []
            for next_posC in possible_moves(posC, POSSIBLE_ROBOT_MOVES):
                if is_in_bull_range(posB, next_posC):
                    # Bull charges towards robot
                    charging_moves = [move for move in possible_moves(posB, POSSIBLE_BULL_MOVES)
                                      if calculate_distance(move, next_posC) < calculate_distance(posB, next_posC)]
                    if charging_moves:
                        expected_value = sum(T_star[(next_posB, next_posC)] for next_posB in charging_moves) / len(charging_moves)
                    else:
                        expected_value = T_star[(posB, posC)]
                else:
                    # Bull moves randomly
                    random_moves = possible_moves(posB, POSSIBLE_BULL_MOVES)
                    expected_value = sum(T_star[(next_posB, next_posC)] for next_posB in random_moves) / len(random_moves)

                expected_values.append(1 + expected_value)  # Add 1 for the current round

            # Update T* for the state (posB, posC)
            min_expected_value = min(expected_values) if expected_values else float('inf')
            new_T_star[(posB, posC)] = min_expected_value

            # Track the maximum change for convergence
            max_change = max(max_change, abs(new_T_star[(posB, posC)] - T_star[(posB, posC)]))

    T_star = new_T_star
    iteration += 1
    print(f"Iteration {iteration}: max change = {max_change}")
    converged = max_change < threshold

# Output the T* value for the original configuration
T_star_initial = T_star[(ROBOT_POSITION, BULL_POSITION)]
print(f"The minimal expected number of rounds to corral the bull from the initial configuration is {T_star_initial:.2f}")
