import random
import sys

WORDS = [
    "python",
    "hangman",
    "computer",
    "programming",
    "friendly",
    "desktop",
    "keyboard",
    "internet",
    "puzzle",
    "challenge",
]

HANGMAN_PICS = [
    "\n   +---+\n       |\n       |\n       |\n      ===",
    "\n   +---+\n   O   |\n       |\n       |\n      ===",
    "\n   +---+\n   O   |\n   |   |\n       |\n      ===",
    "\n   +---+\n   O   |\n  /|   |\n       |\n      ===",
    "\n   +---+\n   O   |\n  /|\\  |\n       |\n      ===",
    "\n   +---+\n   O   |\n  /|\\  |\n  /    |\n      ===",
    "\n   +---+\n   O   |\n  /|\\  |\n  / \\  |\n      ===",
]


def choose_word():
    return random.choice(WORDS)


def get_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""
    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting game.")
        sys.exit(0)


def display_game_state(missed_letters, correct_letters, secret_word):
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    print("Missed letters:", " ".join(missed_letters))

    blanks = ["_" for _ in secret_word]
    for i, letter in enumerate(secret_word):
        if letter in correct_letters:
            blanks[i] = letter

    print("".join(blanks))
    print()


def get_guess(already_guessed):
    while True:
        guess = get_input("Guess a letter: ").lower().strip()
        if not guess:
            print("No input detected. Please type a letter.")
        elif len(guess) != 1:
            print("Please enter a single letter.")
        elif not guess.isalpha():
            print("Please enter a LETTER.")
        elif guess in already_guessed:
            print("You have already guessed that letter. Choose again.")
        else:
            return guess


def play_again():
    while True:
        answer = get_input("Do you want to play again? (yes or no): ").strip().lower()
        if answer.startswith("y"):
            return True
        if answer.startswith("n"):
            return False
        print("Please answer 'yes' or 'no'.")


def play_game():
    if not sys.stdin.isatty():
        print("Please run this game in a terminal so it can accept input.")
        return

    print("Welcome to Hangman!")
    missed_letters = ""
    correct_letters = ""
    secret_word = choose_word()
    game_over = False

    while True:
        display_game_state(missed_letters, correct_letters, secret_word)

        guess = get_guess(missed_letters + correct_letters)

        if guess in secret_word:
            correct_letters += guess

            found_all_letters = True
            for letter in secret_word:
                if letter not in correct_letters:
                    found_all_letters = False
                    break

            if found_all_letters:
                print(f"Yes! The secret word is '{secret_word}'! You have won!")
                game_over = True
        else:
            missed_letters += guess

            if len(missed_letters) == len(HANGMAN_PICS) - 1:
                display_game_state(missed_letters, correct_letters, secret_word)
                print(f"You have run out of guesses! The word was '{secret_word}'.")
                game_over = True

        if game_over:
            if play_again():
                missed_letters = ""
                correct_letters = ""
                game_over = False
                secret_word = choose_word()
            else:
                print("Thanks for playing Hangman!")
                break


if __name__ == "__main__":
    play_game()
