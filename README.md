<center><h1> Simple Battleship Game </h1></center>

A battle ship game in Python with a SQLite database to store users and scores.

## How to play

- Start the program with `python main.py`.
- On first run the program will:
    * Create a new database.
    * Ask the user to enter a username and password to create their first user.
    * It will then launch the game
- After that, a menu will appear on launch asking the user what they want to do:
    * Login
    * Create another user
    * Reset user password
    * Check a user's scores
    * Exit
- Once the user chosen their option, the game is launched.
- Two grid positions are picked, one for the user and one for the computer.
- The user is then shown a grid and asked to guess where the computer's battleship is
- If the user's guess is wrong the computer gets to guess, if the computer guesses wrong the game continues.
- If the user's guess is right, their "wins" score in the database is updated, if the computer guesses right, their "losses" score in the database is updated.
