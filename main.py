import random
import re
import os
import sys

from db_actions import *


def main():
    """
    Main function that go between all functions
    """

    # results = SearchDatabase().search_all()

    # for item in results:
    #     print(item)

    if not os.path.exists("battleship-database"):
        logged_in_user = first_run()
    else:
        logged_in_user = menu_screen()

    comp, user = get_grid_positions()

    game_continue = True
    usr_guesses = []
    comp_guesses = []

    while(game_continue):
        game_continue, user_guess = get_user_guess(comp, user, usr_guesses, logged_in_user)
        # TODO: Figure out why this while loop is not breaking when game_continue == False
        if game_continue == False:
            break
        usr_guesses.append(user_guess)
        
        game_continue, comp_guess = get_comp_guess(user, comp_guesses, logged_in_user)
        if game_continue == False:
            break
        comp_guesses.append(comp_guess)
        
        display_updated_user_grid(usr_guesses)
        display_updated_comp_grid(comp_guesses, user)


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

    loop_menu = True

    while(loop_menu):
        print("******************************************************")
        print("What would you like to do?")
        print("1) Login")
        print("2) Create User")
        print("3) Reset Password")
        print("4) Check My Scores")
        print("0) Exit")
        print("******************************************************")
        
        menu_input = input()

        if menu_input == "1":
            logged_in_user = login_screen()
            loop_menu = False
        elif menu_input == "2":
            logged_in_user = create_user_screen()
            loop_menu = False
        elif menu_input == "3":
            reset_pw_screen()
        elif menu_input == "4":
            check_user_score()
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
    
    try:
        username = input("Enter username:\t")
        pw = input("Enter password:\t")

        CreateUser(username, pw).add()

        return username
    except(Exception):
        print("USERNAME ALREADY EXISTS")
        menu_screen()


def reset_pw_screen():
    """
    Resets the password for the inputted user

    :return prints to screen:
    """
    user = input("Please enter your username:\t")

    username_exists = SearchDatabase(user).search_users()

    if username_exists == "does not exist":
        print("******************************************************")
        print("USERNAME DOES NOT EXIST")
        menu_screen()

    pw = input("Please enter your new password:\t")

    UpdateDatabase(user,pw).reset_password()

    print("Password Reset")


def check_user_score():
    """
    Displays the scores for the inputted user.

    :return prints to screen:
    """
    user = input("Please enter your username:\t")

    username_exists = SearchDatabase(user).search_users()

    if username_exists == "does not exist":
        print("******************************************************")
        print("USERNAME DOES NOT EXIST")
        menu_screen()

    results = SearchDatabase(user).search_scores()

    print("WINS:\t" + str(results[0]) + "\nLOSSES:\t" + str(results[1]) + "\n\n")


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

    # print("Computer Location " + comp)

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


def get_user_guess(comp_loc, usr_loc, usr_guesses, logged_in_user):
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

    :param the computer's grid position, the user's grid position, the user's past guesses:
    
    :return if user wins:
                prints to screen, boolean value of false for game to continue
            else:
                prints to screen, boolean value of true for game to continue, 
                users guess to be added to a list
    """

    usr_guess_good = False
    
    while not (usr_guess_good):
        usr_guess = input("Please enter your guess:\n").upper()

        if usr_guess == usr_loc:
            print("That's your spot, try again")
        elif not re.match("^[A-D][1-4]$", usr_guess):
            print("Please enter it in the right format")
        elif usr_guess in usr_guesses:
            print("You already guessed that spot")
        else:
            usr_guess_good = True

    if usr_guess == comp_loc:
        print("wow big hit, user wins")
        UpdateDatabase(logged_in_user).user_win()
        return False, usr_guess
    else:
        print("thats a miss!")
        return True, usr_guess


def get_comp_guess(usr_loc, comp_guesses, logged_in_user):
    """
    Gets the computer to guess and then sees if there guess is correct or not

    Comp guesses a random coord
    if the guess is in the comp_guesses list:
        the comp has already guessed that position and is told to guess again
    else:
        If the comp guess is the same as the user location:
            Prints to screen and the user wins
            Will deduct points from the users database
        else:
            game continues.

    :param the user's grid position, the computer guesses in a list:
    
    :return if comp wins:
                prints to screen, boolean value of false for game to continue
            else:
                prints to screen, boolean value of true for game to continue, 
                comp guess to be added to a list
    """

    comp_guess_good = False

    while not comp_guess_good:
        options_rows = ["A", "B", "C", "D"]

        comp_guess = options_rows[random.randint(0,3)] + str(random.randint(1,4))

        if comp_guess not in comp_guesses:
            comp_guess_good = True

    print("Computer guessed:\t" + comp_guess)

    if comp_guess == usr_loc:
        UpdateDatabase(logged_in_user).user_losses()
        print("Comp Wins")
        return False, comp_guess
    else:
        return True, comp_guess  


def display_updated_user_grid(guesses):
    """
    Prints the updated grid with hit locations to the screen.

    Adds an X into the position where the user guessed so they can see what they've guessed.

    As the grid is printed the current coord is stored, and if it is in the list of guesses, an X is used instead of a -

    :params a list of all the guesses the user has made:

    :return Prints to screen:
    """

    options_rows = ["A", "B", "C", "D"]

    print("\nUSER GRID")

    print("  1 2 3 4")

    for x in range(4):
        current_row = options_rows[x]
        print(current_row, end=" ")
        for y in range(4):
            # need to add 1 to the y value as they start from 0 instead of 1
            current_coord = current_row + str(y+1)
            if current_coord in guesses:
                print("X ", end="")
            else:
                print("- ", end="")
            if y == 3:
                print("\n")


def display_updated_comp_grid(guesses, user_loc):
    """
    Prints the updated grid with hit locations to the screen.

    Adds an X into the position where the comp guessed.

    As the grid is printed the current coord is stored, and if it is in the list of guesses, an X is used instead of a -

    If the current coord is equal to the user location, an O is used instead of a -

    :params a list of all the guesses the comp has made:

    :return Prints to screen:
    """

    options_rows = ["A", "B", "C", "D"]

    print("\nCOMPUTER GRID")

    print("  1 2 3 4")

    for x in range(4):
        current_row = options_rows[x]
        print(current_row, end=" ")
        for y in range(4):
            # need to add 1 to the y value as they start from 0 instead of 1
            current_coord = current_row + str(y+1)
            if current_coord in guesses:
                print("X ", end="")
            elif current_coord == user_loc:
                print("O ", end="")
            else:
                print("- ", end="")
            if y == 3:
                print("\n")


if __name__ == "__main__":
    main()