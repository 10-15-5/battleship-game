import random
import re
import os


def main():
    comp, user = get_grid_positions()

    game_continue = True
    usr_guesses = []

    while(game_continue):
        game_continue, guess = get_user_guess(comp, user)
        usr_guesses.append(guess)
        display_updated_grid(usr_guesses)


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