#!/usr/bin/env python3
"""Simple Number Guessing Game

Run this script and try to guess the secret number. Enter 'q' or 'quit'
to exit at any time. After each round you'll be offered to play again.
"""

import random


def play(low: int = 1, high: int = 100) -> bool:
	"""Play one round of the guessing game.

	Returns True if the round completed normally (player guessed the number),
	or False if the player chose to quit early.
	"""
	secret = random.randint(low, high)
	attempts = 0
	print(f"\nI'm thinking of a number between {low} and {high}.")
	print("Type 'q' or 'quit' to exit at any time.")

	while True:
		guess = input(f"Enter your guess ({low}-{high}): ").strip()
		if guess.lower() in {"q", "quit", "exit"}:
			print("Exiting current game.")
			return False

		try:
			value = int(guess)
		except ValueError:
			print("Please enter a valid integer or 'q' to quit.")
			continue

		if value < low or value > high:
			print(f"Out of range — enter a number between {low} and {high}.")
			continue

		attempts += 1
		if value < secret:
			print("Too low. Try again.")
		elif value > secret:
			print("Too high. Try again.")
		else:
			print(f"Correct! You guessed the number in {attempts} attempts.")
			return True


def main() -> None:
	print("Number Guessing Game — try to guess the secret number!")
	while True:
		completed = play()
		if completed is False:
			break

		again = input("Play again? (y/n): ").strip().lower()
		if again not in {"y", "yes"}:
			print("Thanks for playing — goodbye!")
			break


if __name__ == "__main__":
	main()

