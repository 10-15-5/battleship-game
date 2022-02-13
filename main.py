import random
import re
import os
import sys

from db_actions import *


def main():
    """
    Main function that go between all functions
    """

    if not os.path.exists("battleship-database"):
        logged_in_user = first_run()
    else:
        logged_in_user = menu_screen()

    # comp, user = get_grid_positions()

    # game_continue = True
    # usr_guesses = []

    # while(game_continue):
    #     game_continue, guess = get_user_guess(comp, user)
    #     usr_guesses.append(guess)
    #     display_updated_grid(usr_guesses)


def first_run():
    """
    Creates database on first run.

    If the database file does not exist, this function is run.
    Creates a database, using the db_actions file, called "battleship-database".
    Asks the user to enter a username and password to create the first user.
    Adds these details to the database.
    Returns the username entered by the user as this will tell the rest of the
    program that this user is logged in.

    :return username of logged in user:
    """

    CreateDatabase().create()

    print("Creating first user")

    username = input("Enter a username:\t")
    pw = input("Enter a password:\t")

    CreateUser(username, pw).add()

    return username


def menu_screen():
    """
    Prints the menu screen to the console and takes in user input.

    Prints the menu in a loop until the user enters a correct command.
    1) to login
    2) to create a new user
    3) reset password
    0) exit program

    :return username of logged in user
    """

    print("******************************************************")
    print("What would you like to do?")
    print("1) Login")
    print("2) Create User")
    print("3) Reset Password")
    print("0) Exit")
    print("******************************************************")

    loop_menu = True

    while(loop_menu):
        menu_input = input()

        if menu_input == "1":
            logged_in_user = login_screen()
            loop_menu = False
        elif menu_input == "2":
            logged_in_user = create_user_screen()
            loop_menu = False
        elif menu_input == "3":
            # logged_in_user = reset_pw_screen()
            # loop_menu = False
            print("Not done yet")
        elif menu_input == "0":
            sys.exit(0)

    return logged_in_user


def login_screen():
    """
    Prints the login screen to the console for the user to enter username and pw.

    Gets user input of what user and pw they want to login as.
    Checks the database to make sure that the username exists.
    if username does not exist:
        message is displayed on screen and the user is sent back to the original menu
    else:
        Checks the database to make sure the entered pw is correct for that user
        if pw is not correct:
            message is displayed on screen and the user is sent back to the original menu
        else:
            user is logged in

    :return username of logged in user
    """
    
    print("******************************************************")
    user = input("Enter username:\t")
    pw = input("Enter password:\t")

    username_exists = LoginUser(user, pw).check_users()

    if not username_exists:
        print("******************************************************")
        print("USERNAME INCORRECT")
        menu_screen()
    else:
        pw_correct = LoginUser(user, pw).check_pw()

        if not pw_correct:
            print("******************************************************")
            print("PASSWORD FOR " + user + " INCORRECT")
            menu_screen()
        else:
            print("******************************************************")
            print("WELCOME " + user)
            print("******************************************************")
            return user


def create_user_screen():
    """
    Prints the create user screen to the console for the user to input a username
    and pw.

    Adds credentials to the databse so the user can login in future.

    :return username of logged in user:
    """

    print("******************************************************")
    print("CREATING NEW USER")
    print("******************************************************")
    
    username = input("Enter username:\t")
    pw = input("Enter password:\t")

    CreateUser(username, pw).add()

    return username


def get_grid_positions():
    """
    Gets randomly assigned grid positions for the user and computer.

    The random library sets 2 grid positions, 1 for the user and 1 for the comp.
    The grid positions are between A1 and D4.
    If the computer and the user end up having the same grid position.
    The user gets assigned a new grid position.
    Prints the users grid postition to the screen for the user to take note of.
    Goes into the initial grid function to print the initial grid to the screen.

    :return computer grid position, user grid position:
    """

    comp = ""
    user = ""

    options_rows = ["A", "B", "C", "D"]

    comp = options_rows[random.randint(0,3)] + str(random.randint(1,4))

    user = options_rows[random.randint(0,3)] + str(random.randint(1,4))

    while(comp == user):
        user = options_rows[random.randint(0,3)] + str(random.randint(1,4))

    print("YOUR LOCATION IS: " + user)

    display_initial_grid(options_rows) 

    return comp, user


def display_initial_grid(options_rows):
    """
    Displays the initial grid on screen for the user to see

    :return Prints to screen:
    """
    
    print("  1 2 3 4")
    for x in range(4):
        print(options_rows[x] + " " + ('- '*4) + "\n")


def get_user_guess(comp_loc, usr_loc):
    """
    Gets the user to input a guess and lets them know if it's a hit.

    The user is asked to input a grid position that they think the computer is in.
    The guess is validated to make sure it is in the grid and the user is not 
    guessing something like Z8 or WR678.
    If the user guess is the same as the computer location:
        Prints to screen and the user wins
        Will add points the users database then
    else:
        prints that they missed and the game continues.

    :param the computer's grid position, the user's grid position:
    
    :return if user wins:
                prints to screen, boolean value of false for game to continue
            else:
                prints to screen, boolean value of true for game to continue, 
                users guess to be added to a list
    """

    usr_guess_flag = False
    
    while not (usr_guess_flag):
        usr_guess = input("Please enter your guess (A1, B3, C1, D2):\n")

        usr_guess_flag = validate_guess(usr_guess)

    if re.search(usr_guess, comp_loc, re.IGNORECASE):
        print("wow big hit, user wins")
        return False
    # elif usr_guess == usr_loc:
    #     print("That's your spot, try again")
    else:
        print("thats a miss!")
        return True, usr_guess


def validate_guess(guess):
    """
    Validates the users guess.

    Checks the guess against a regex function.
    The guess has to be in the pattern of 1 letter, a to d or A to D, and 1 number,
    1 to 4.
    
    :param Takes in the user's guess:
    
    :return if guess is validated:
                boolean value that the guess is good:
            else:
                prints to console telling them the guess is incorrect:
    """

    if re.match("^[a-dA-D][1-4]$", guess):
        return True
    else:
        print("Error with guess. Please only enter a guess from A1 - D4.\n")


def display_updated_grid(guesses):
    """
    Prints the updated grid with hit locations to the screen.

    Adds an X into the position where the user guessed so they can see what they've guessed.

    :params a list of all the guesses the user has made:

    :return Prints to screen:
    """

    options_rows = ["A", "B", "C", "D"]

    # if re.search(guesses[y][0], options_rows[x], re.IGNORECASE):

    print("  1 2 3 4")

    for x in range(4):
        print(options_rows[x], end=" ")
        for y in range(4):
            print("- ", end="")
            if y == 3:
                print("\n")


if __name__ == "__main__":
    main()