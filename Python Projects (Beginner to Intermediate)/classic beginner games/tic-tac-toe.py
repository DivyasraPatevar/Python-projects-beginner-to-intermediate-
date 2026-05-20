import random

BOARD_TEMPLATE = "\n {0} | {1} | {2}\n---+---+---\n {3} | {4} | {5}\n---+---+---\n {6} | {7} | {8}\n"


def display_board(board):
    print(BOARD_TEMPLATE.format(*board))


def check_winner(board, player):
    win_lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_lines)


def board_full(board):
    return all(space != " " for space in board)


def get_player_move(board):
    while True:
        move = input("Enter your move (1-9): ").strip()
        if not move.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        index = int(move) - 1
        if index < 0 or index > 8:
            print("Move must be between 1 and 9.")
            continue
        if board[index] != " ":
            print("That position is already taken. Choose another.")
            continue
        return index


def get_computer_move(board):
    available = [idx for idx, value in enumerate(board) if value == " "]
    return random.choice(available)


def play_game():
    board = [" "] * 9
    current_player = "X"
    print("Welcome to Tic Tac Toe!")
    print("You are X and the computer is O.")
    display_board([str(i + 1) for i in range(9)])

    while True:
        display_board(board)

        if current_player == "X":
            index = get_player_move(board)
        else:
            print("Computer is choosing a move...")
            index = get_computer_move(board)

        board[index] = current_player

        if check_winner(board, current_player):
            display_board(board)
            if current_player == "X":
                print("Congratulations! You win!")
            else:
                print("Computer wins. Better luck next time!")
            break

        if board_full(board):
            display_board(board)
            print("It's a tie!")
            break

        current_player = "O" if current_player == "X" else "X"


def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing Tic Tac Toe!")
            break


if __name__ == "__main__":
    main()
