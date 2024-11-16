import random
import sys
import hmac
import hashlib

def hmac_hash(secret_key, msj):
    return hmac.new(secret_key.encode(), str(msj).encode(), hashlib.sha256).hexdigest()

def validate_args(args):
    if len(args) < 3:
        return False, "Error: At least three data sets are required."

    sets = []
    for arg in args:
        try:
            dice = list(map(int, arg.split(',')))
            if len(dice) != 6:
                return False, "Error: Each data set must contain exactly 6 values"
            sets.append(dice)
        except ValueError:
            return False, "Error: Each data set must contain exactly 6 comma-separated values"
    return True, sets

def first_move():
    secret_key = str(random.randint(1, 1000))
    computer_choice = random.randint(0, 1)
    hmac_proof = hmac_hash(secret_key, computer_choice)

    print(f"I selected a random value in range 0 - 1 (HMAC={hmac_proof})")
    while True:
        user_guess = input("Try to guess my selection. \n0 - 0\n1 - 1\nX - exit\nH - help\nYour selection: ")
        if user_guess.lower() == 'x':
            print("Game Over")
            exit()
        elif user_guess.lower() == 'h':
            print("Help Menu: Select a number, computer work automatic")
        else:
            try:
                user_guess = int(user_guess)
                if user_guess not in (0, 1):
                    raise ValueError
                break
            except ValueError:
                print("Invalid selection. Try again.")

    print(f"My selection: {computer_choice} (KEY= {hmac_proof}).")
    if user_guess == computer_choice:
        print("You won, make the first move.")
        return True
    else:
        print("You lost, I made the first move.")
        return False

def select_dice(sets, player):
    if player == "user":
        while True:
            print("Choose your dice:")
            for i, dice in enumerate(sets):
                print(f"{i} - {dice}")
            print("X: Exit")
            print("H: Help")
            choice = input("Your selection: ")

            if choice.lower() == "x":
                print("Game Over")
                exit()
            elif choice.lower() == "h":
                print("Help Menu: Select a number, computer work automatic")
            else:
                try:
                    choice = int(choice)
                    if choice < 0 or choice >= len(sets):
                        raise IndexError
                    return sets.pop(choice)
                except (ValueError, IndexError):
                    print("Invalid selection.")
    else:
        computer_choice = random.choice(sets)
        sets.remove(computer_choice)
        print(f"I choose the {computer_choice} dice")
        return computer_choice

def roll_dice(dice, secret_key, player, opponent_dice):
    computer_number = random.randint(0, 5)
    hmac_proof = hmac_hash(str(secret_key), computer_number)
    print(f"I selected a random value in the range 0 - 5. (HMAC={hmac_proof})")

    while True:
        user_guess = input(
            "Add your number modulo 6. \n"
            "0 - 0\n"
            "1 - 1\n"
            "2 - 2\n"
            "3 - 3\n"
            "4 - 4\n"
            "5 - 5\n"
            "X - exit\n"
            "H - help\n"
            "Your selection: "
        )

        if user_guess.lower() == "x":
            print("Game Over")
            exit()
        elif user_guess.lower() == "h":
            print("Help Menu: Select a number, computer work automatic")
        else:
            try:
                user_number = int(user_guess)
                if user_number not in range(6):
                    raise ValueError
                break
            except ValueError:
                print("Invalid selection. Try again.")

    result = (computer_number + user_number) % 6
    print(f"My number is {computer_number} (KEY={hmac_proof})")
    print(f"The result is {computer_number} + {user_number} = {result} (mod 6)")

    computer_throw = dice[result]
    print(f"My throw is {computer_throw}.")
    
    user_throw = opponent_dice[user_number]
    print(f"Your throw is {user_throw}.")

    # Decide the winner
    if computer_throw > user_throw:
        print(f"I win ({computer_throw} > {user_throw})!")
    elif computer_throw < user_throw:
        print(f"You win ({user_throw} > {computer_throw})!")
    else:
        print(f"It's a draw ({user_throw} == {computer_throw})!")

    return user_throw, computer_throw

def main():
    if len(sys.argv) < 4:
        print("Error: Not enough arguments")
        sys.exit(1)
    
    valid, result = validate_args(sys.argv[1:])
    if not valid:
        print(result)
        sys.exit(1)

    sets = result
    print("Welcome to SetGame")
    print("Let's determine who makes the first move")
    init = first_move()
    key = random.randint(1, 1000)

    if init:
        user_dice = select_dice(sets, "user")
        computer_dice = select_dice(sets, "computer")
        roll_dice(user_dice, key, init, computer_dice)
    else:
        computer_dice = select_dice(sets, "computer")
        user_dice = select_dice(sets, "user")
        roll_dice(computer_dice, key, init, user_dice)

if __name__ == "__main__":
    main()