# Project: Dragon Ball Z Power Level Showdown!
# Version :  0.1
# Date    :  4/17/25
# Author: Jody Ingram
# Pre-reqs: Requires Python to run. Python.org
# You choose between Goku or Vegeta and the game determines which character is stronger based on their power levels.

goku_power = 9001
vegeta_power = 9040

print("Welcome to the Dragon Ball Z Power Level Showdown!")
print("Goku's power level:", goku_power)
print("Vegeta's power level:", vegeta_power)

# Prompt the player
guess = input("Who do you think is stronger: Goku or Vegeta? ").strip().lower()

# Validate player's input
if guess not in ["goku", "vegeta"]:
    print(f"No one asked you about '{guess.capitalize()}', please try again!")
else:
    # Determine who is actually stronger
    if goku_power > vegeta_power:
        winner = "goku"
    elif vegeta_power > goku_power:
        winner = "vegeta"
    else:
        winner = "tie"

    # Respond to the player
    if guess == winner:
        print(f"You're right! {guess.capitalize()} is stronger!")
    elif winner == "tie":
        print("It's actually a tie! Their power levels are exactly the same!")
    else:
        print(f"Actually, {winner.capitalize()} is stronger than {guess.capitalize()}.")

    # Gotta have the DBZ flair; you know you can hear it in their voices
    if winner == "goku":
        print("Goku wins! It's over 9000!!!")
    elif winner == "vegeta":
        print("Vegeta wins! The prince of all Saiyans reigns supreme!")
