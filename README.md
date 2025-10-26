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
    Open your terminal or Command Prompt and clone this repository:
    ```bash
    git clone git@github.com:Aurlaze/minesweeper-ai.git
    cd minesweeper-ai
    ```
    *(Note: The folder name might be `pygame-minesweeper-1.0.11` if you used the tarball)*

2.  **Create Virtual Environment:**
    Navigate to your project directory and create a virtual environment. It's crucial to use one to manage dependencies.
    ```bash
    # Create the environment (e.g., named 'minesweeper_dev_env')
    python -m venv minesweeper_dev_env
    ```
    *(Note: On some systems, you might need to use `python3` instead of `python`)*

3.  **Activate Virtual Environment:**
    You need to activate the environment before installing packages. The command depends on your operating system and shell.

    * **Windows (Command Prompt `cmd.exe`):**
      ```cmd
      minesweeper_dev_env\Scripts\activate.bat
      ```

    * **Windows (PowerShell):**
      ```powershell
      .\minesweeper_dev_env\Scripts\Activate.ps1
      ```
      *(Note: If you get an error in PowerShell about execution policies, you may need to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first.)*

    * **Linux / macOS / WSL (Bash/Zsh):**
      ```bash
      source minesweeper_dev_env/bin/activate
      ```
    Your terminal prompt should now start with `(minesweeper_dev_env)`.

4.  **Install Dependencies (Editable Mode):**
    This command installs the game, its dependencies (like Pygame and PuLP), and links them to your local source code so your changes take effect. The `--no-build-isolation` flag is needed for compatibility with this older package.
    ```bash
    # Make sure you are inside the project folder
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
    *(Note: On Windows, if the `minesweeper` command isn't found directly, you might need to run it as a module: `python -m minesweeper basic`)*

2.  **Make the First Move:**
    Click anywhere on the grid to reveal the initial area. This gives the AI its first clues.

3.  **Activate the AI:**
    Click the **smiley face button** 😃 at the top of the game window. The AI will take over and automatically solve the rest of the board.

### Deactivating the Environment

When you're finished working, you can deactivate the virtual environment by simply running:
```bash
deactivate

## Credits & References

* **Base Game:** This project modifies the excellent `pygame-minesweeper` package.
    * PyPI: [https://pypi.org/project/pygame-minesweeper/](https://pypi.org/project/pygame-minesweeper/)
* **AI Inspiration:** The core AI logic using Constraint Programming (PuLP) and the integration technique were inspired by:
    * Alex Brou's YouTube Video: ["I coded the Perfect AI for Minesweeper"](https://youtu.be/gKMZbzl0V7U)
    * Alex Brou's Medium Article: ["The perfect Minesweeper AI: an approach using Linear/Constraint Programming"](https://medium.com/@alexbrou/the-perfect-minesweeper-ai-an-approach-using-linear-constraint-programming-1d4cf8cc8101)
