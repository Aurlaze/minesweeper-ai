import pulp
import random


def get_neighbors(cell, height, width):
    """Helper function to get valid neighbor coordinates."""
    neighbors = []
    for r_offset in [-1, 0, 1]:
        for c_offset in [-1, 0, 1]:
            if r_offset == 0 and c_offset == 0:
                continue
            ni, nj = cell[0] + r_offset, cell[1] + c_offset
            if 0 <= ni < height and 0 <= nj < width:
                neighbors.append((ni, nj))
    return neighbors


# --- BRAIN 1: THE FAST BRAIN (FOR SPEED) ---
def find_simple_moves(height, width, known_clues, unknown_cells, flagged_cells):
    """
    Finds "obvious" safe moves or new mines without using the heavy solver.
    """
    unknown_set = set(unknown_cells)
    flagged_set = set(flagged_cells)

    new_safes = set()
    new_mines = set()  # We don't use this yet, but it's good to have

    for cell, count in known_clues.items():
        cell_neighbors = get_neighbors(cell, height, width)

        hidden_neighbors = []
        num_flagged_neighbors = 0

        for neighbor in cell_neighbors:
            if neighbor in unknown_set:
                hidden_neighbors.append(neighbor)
            elif neighbor in flagged_set:
                num_flagged_neighbors += 1

        # Rule 1: "All-Flagged"
        if count == num_flagged_neighbors and hidden_neighbors:
            for neighbor in hidden_neighbors:
                new_safes.add(neighbor)

        # Rule 2: "All-Hidden"
        if (
            count == (len(hidden_neighbors) + num_flagged_neighbors)
            and hidden_neighbors
        ):
            for neighbor in hidden_neighbors:
                new_mines.add(neighbor)

    return new_safes, new_mines


# --- BRAIN 2: THE HEAVY BRAIN (FOR ACCURACY) ---
def find_safe_move(height, width, known_clues, unknown_cells):
    """
    Uses PuLP to find a guaranteed safe move.
    """
    problem = pulp.LpProblem("MinesweeperSolver", pulp.LpMinimize)
    board_vars = {}
    for cell in unknown_cells:
        board_vars[cell] = pulp.LpVariable(f"cell_{cell[0]}_{cell[1]}", cat="Binary")

    for cell, count in known_clues.items():
        cell_neighbors = get_neighbors(cell, height, width)

        relevant_neighbor_vars = []
        for neighbor in cell_neighbors:
            if neighbor in board_vars:
                relevant_neighbor_vars.append(board_vars[neighbor])

        if relevant_neighbor_vars:
            problem += pulp.lpSum(relevant_neighbor_vars) == count, f"Clue_at_{cell}"

    for cell_to_test in unknown_cells:
        if cell_to_test not in board_vars:
            continue

        test_problem = problem.copy()
        test_problem += board_vars[cell_to_test] == 1, f"Assumption_{cell_to_test}"

        solver = pulp.PULP_CBC_CMD(msg=False)
        status = test_problem.solve(solver)

        if status == pulp.LpStatusInfeasible:
            return cell_to_test  # Guaranteed safe move

    return None  # No guaranteed safe move found


# --- BRAIN 3: THE SMART GUESSTIMATOR (REVISED) ---
def find_safest_guess(
    height, width, known_clues, unknown_cells, flagged_cells, total_mines
):
    """
    Finds the cell with the lowest probability of being a mine,
    or picks a random cell if probabilities are equal or unhelpful.
    """

    # 1. First, check for a "local" probability.
    min_probability = 1.0  # Start with 100%
    best_guess_candidates = []  # Store potential best guesses

    unknown_set = set(unknown_cells)
    flagged_set = set(flagged_cells)

    for cell, count in known_clues.items():
        cell_neighbors = get_neighbors(cell, height, width)

        hidden_neighbors = []
        num_flagged_neighbors = 0

        for neighbor in cell_neighbors:
            if neighbor in unknown_set:
                hidden_neighbors.append(neighbor)
            elif neighbor in flagged_set:
                num_flagged_neighbors += 1

        # We only care about "active" clues that still border hidden cells
        if not hidden_neighbors:
            continue

        # Avoid division by zero
        if len(hidden_neighbors) == 0:
            continue

        probability = (count - num_flagged_neighbors) / len(hidden_neighbors)

        # Ensure probability is valid (can be < 0 if flags are wrong)
        probability = max(0.0, min(1.0, probability))

        if probability < min_probability:
            min_probability = probability
            best_guess_candidates = hidden_neighbors  # Start a new list
        elif probability == min_probability:
            # Add these equally likely candidates
            best_guess_candidates.extend(hidden_neighbors)

    # Remove duplicates if multiple clues pointed to the same cells
    if best_guess_candidates:
        best_guess_candidates = list(set(best_guess_candidates))
        return random.choice(best_guess_candidates)

    # 2. If no local preference, just pick ANY unknown cell if one exists.
    #    The heavy/simple solvers should handle cases where all remaining are mines.
    if unknown_cells:
        return random.choice(unknown_cells)

    # 3. Only return None if there are truly no cells left to guess.
    return None
