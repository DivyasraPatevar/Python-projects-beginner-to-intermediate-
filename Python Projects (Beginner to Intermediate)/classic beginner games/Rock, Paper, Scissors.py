import random

OPTIONS = ["rock", "paper", "scissors"]
CHOICE_ART = {
    "rock": "rock",
    "paper": "paper",
    "scissors": "scissors",
}


def get_player_choice():
    print("\nChoose your move:")
    print("  1) Rock")
    print("  2) Paper")
    print("  3) Scissors")
    print("  Q) Quit")

    while True:
        selection = input("Enter 1, 2, 3, or Q: ").strip().lower()
        if selection == "1" or selection == "rock":
            return "rock"
        if selection == "2" or selection == "paper":
            return "paper"
        if selection == "3" or selection == "scissors":
            return "scissors"
        if selection == "q" or selection == "quit":
            return "quit"
        print("Invalid input. Please enter 1, 2, 3, or Q.")


def get_computer_choice():
    return random.choice(OPTIONS)


def determine_winner(player, computer):
    if player == computer:
        return "tie"
    if (player == "rock" and computer == "scissors") or (
        player == "paper" and computer == "rock"
    ) or (player == "scissors" and computer == "paper"):
        return "player"
    return "computer"


def print_result(player_choice, computer_choice, winner, player_score, computer_score):
    print(f"\nYou chose: {player_choice}")
    print(f"Computer chose: {computer_choice}")

    if winner == "tie":
        print("Result: It's a tie!")
    elif winner == "player":
        print("Result: You win this round!")
    else:
        print("Result: Computer wins this round.")

    print(f"\nScore -> You: {player_score} | Computer: {computer_score}")


def play_game():
    print("Welcome to Rock, Paper, Scissors!")
    print("Type 1, 2, 3, or Q when prompted.")

    player_score = 0
    computer_score = 0

    while True:
        player_choice = get_player_choice()
        if player_choice == "quit":
            print("\nGoodbye! Thanks for playing.")
            break

        computer_choice = get_computer_choice()
        winner = determine_winner(player_choice, computer_choice)

        if winner == "player":
            player_score += 1
        elif winner == "computer":
            computer_score += 1

        print_result(player_choice, computer_choice, winner, player_score, computer_score)

        if player_score >= 3 or computer_score >= 3:
            if player_score > computer_score:
                print("\nCongratulations! You won the game!")
            else:
                print("\nThe computer won the game. Try again!")
            break

        input("\nPress Enter to play the next round...")


if __name__ == "__main__":
    play_game()
