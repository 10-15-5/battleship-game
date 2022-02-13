import random
import re
import os
import sys

from db_actions import *


def main():
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
    CreateDatabase().create()

    print("Creating first user")

    username = input("Enter a username:\t")
    pw = input("Enter a password:\t")

    CreateUser(username, pw).add()

    return username


def menu_screen():
    print("******************************************************")
    print("What would you like to do?")
    print("1) Login")
    print("2) Create user")
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
        elif menu_input == "0":
            sys.exit(0)

    return logged_in_user


def login_screen():
    
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
    print("******************************************************")
    print("CREATING NEW USER")
    print("******************************************************")
    
    username = input("Enter username:\t")
    pw = input("Enter password:\t")

    CreateUser(username, pw).add()

    return username


def get_grid_positions():
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
    print("  1 2 3 4")
    for x in range(4):
        print(options_rows[x] + " " + ('- '*4) + "\n")


def get_user_guess(comp_loc, usr_loc):
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
    if re.match("^[a-dA-D][1-4]$", guess):
        return True
    else:
        print("Error with guess. Please only enter a guess from A1 - D4.\n")


def display_updated_grid(guesses):
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