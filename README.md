# Minesweeper AI Solver

This project implements an AI that can automatically play and solve the classic game of Minesweeper. It uses a combination of simple logical deduction, constraint satisfaction programming (via PuLP), and probabilistic guessing to determine safe moves.

The AI is integrated into a modified version of the `pygame-minesweeper` package.

## Features

* **Hybrid Solving:** Uses fast, simple logic for obvious moves and a more powerful PuLP solver for complex situations.
* **Probabilistic Guessing:** Makes educated guesses when logically stuck, improving performance on harder difficulties.
* **Automatic Play:** Can be triggered to solve the board automatically after the first manual move.

## Getting Started

Follow these steps to set up and run the AI on your local machine.

### Prerequisites

* Python 3 (tested with 3.12)
* `git` (for cloning the repository)
* Python's `venv` module (usually included with Python)

### Installation

1.  **Clone the Repository:**
    Open your terminal and clone this repository:
    ```bash
    git clone git@github.com:Aurlaze/minesweeper-ai.git
    cd minesweeper-ai
    ```
    *(Note: The folder name might be `pygame-minesweeper-1.0.11` if you used the tarball)*

2.  **Create and Activate Virtual Environment:**
    It's crucial to use a virtual environment to manage dependencies.
    ```bash
    # Create the environment (e.g., named 'minesweeper_dev_env')
    python3 -m venv minesweeper_dev_env

    # Activate the environment (Linux/macOS/WSL)
    source minesweeper_dev_env/bin/activate
    ```
    Your terminal prompt should now start with `(minesweeper_dev_env)`.

3.  **Install Dependencies (Editable Mode):**
    This command installs the game, its dependencies (like Pygame and PuLP), and links them to your local source code so your changes take effect. The `--no-build-isolation` flag is needed for compatibility with this older package.
    ```bash
    # Make sure you are inside the project folder (e.g., minesweeper-ai or pygame-minesweeper-1.0.11)
    pip install setuptools wheel # Ensure build tools are present
    pip install --no-build-isolation -e .
    pip install pulp # Install the AI's solver dependency
    ```

### Running the AI

1.  **Start the Game:**
    Make sure your virtual environment is active. Run the game with the desired difficulty:
    ```bash
    minesweeper basic
    # Or: minesweeper intermediate
    # Or: minesweeper expert
    ```

2.  **Make the First Move:**
    Click anywhere on the grid to reveal the initial area. This gives the AI its first clues.

3.  **Activate the AI:**
    Click the **smiley face button** 😃 at the top of the game window. The AI will take over and automatically solve the rest of the board.

## Credits & References

* **Base Game:** This project modifies the excellent `pygame-minesweeper` package.
    * PyPI: [https://pypi.org/project/pygame-minesweeper/](https://pypi.org/project/pygame-minesweeper/)
* **AI Inspiration:** The core AI logic using Constraint Programming (PuLP) and the integration technique were inspired by:
    * Alex Brou's YouTube Video: ["I coded the Perfect AI for Minesweeper"](https://youtu.be/gKMZbzl0V7U)
    * Alex Brou's Medium Article: ["The perfect Minesweeper AI: an approach using Linear/Constraint Programming"](https://medium.com/@alexbrou/the-perfect-minesweeper-ai-an-approach-using-linear-constraint-programming-1d4cf8cc8101)
