import random
import sys
from collections import Counter

# ANSI escape codes for colored output
GREEN = '\033[92m'
YELLOW = '\033[93m'
GRAY = '\033[90m'
# To end colour codes
ENDC = '\033[0m'

def load_word_list(filepath="AbdulqadarManasawala_techai_tasks/words.txt"):
    """
    Loads a list of five-letter words from a text file.
    Each word is expected to be on a new line.
    
    Args:
        filepath (str): The path to the word list file.
        
    Returns:
        set: A set of five-letter words. Using a set is
             efficient for word lookups.
    """
    try:
        with open(filepath, 'r') as file:
            # Strip whitespace and convert to lowercase for consistency
            words = {word.strip().lower() for word in file}
        
        # Returning only 5 letter words
        return {word for word in words if len(word) == 5}
    
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found. Please ensure it is in the same directory.")
        sys.exit(1) # Exit the program if the word list is missing

def get_feedback(secret_word, guess):
    """
    Compares the user's guess to the secret word and provides feedback.
    
    Args:
        secret_word (str): The secret word to be guessed.
        guess (str): The user's guess.
        
    Returns:
        tuple: A tuple of colored letters representing the feedback.
               (e.g., ('G', 'Y', 'A', 'G', 'A'))
    """
    feedback = ['' for _ in range(5)]
    # Use a Counter to handle duplicate letters correctly
    secret_counts = Counter(secret_word)
    
    # First pass: Check for correct (green) letters
    for i in range(5):
        if guess[i] == secret_word[i]:
            feedback[i] = GREEN + guess[i].upper() + ENDC
            secret_counts[guess[i]] -= 1
    
    # Second pass: Check for present (yellow) and absent (gray) letters
    for i in range(5):
        if feedback[i]: # Skip if already marked green
            continue
        if guess[i] in secret_counts and secret_counts[guess[i]] > 0:
            feedback[i] = YELLOW + guess[i].upper() + ENDC
            secret_counts[guess[i]] -= 1
        else:
            feedback[i] = GRAY + guess[i].upper() + ENDC

    # Cannot use the single pass approach because:
    # if secret_word is CABLE and guess is AARON
    # then the first A should be YELLOW and second A should be GRAY
    # but in single pass, first A will be YELLOW and second A will be GREEN

    # for i in range(5):
    #     if guess[i] == secret_word[i]:
    #         feedback[i] = GREEN + guess[i].upper() + ENDC 
    #         secret_counts[guess[i]] -= 1
    #     elif guess[i] in secret_counts and secret_counts[guess[i]] > 0:
    #         feedback[i] = YELLOW + guess[i].upper() + ENDC
    #         secret_counts[guess[i]] -= 1
    #     else:
    #         feedback[i] = GRAY + guess[i].upper() + ENDC
    
    return tuple(feedback)

def play_wordle():
    """
    The main game function to run the Wordle game.
    """
    print("\n" + "-" * 20)
    print("Welcome to Command-Line Wordle!")
    print("Guess the five-letter word in six attempts.")
    print(f"[{GREEN}G{ENDC}] Correct letter, correct position.")
    print(f"[{YELLOW}Y{ENDC}] Correct letter, wrong position.")
    print(f"[{GRAY}A{ENDC}] Letter is not in the word.")
    print("-" * 20)
    
    # Load the word list and select a random secret word
    valid_words = load_word_list()
    if not valid_words:
        print("The word list is empty. Please check the file.")
        sys.exit(1)
        
    secret_word = random.choice(list(valid_words))
    
    attempts = 0
    max_attempts = 6
    guesses_history = []
    
    while attempts < max_attempts:
        guess = input(f"Attempt {attempts + 1}/{max_attempts}: Enter your guess: ").strip().lower()
        
        # Validate the user's input
        if len(guess) != 5:
            print(f"Your guess must be a five-letter word. Try again.\n")
            continue
            
        if guess not in valid_words:
            print(f"'{guess}' is not in the word list. Try again.\n")
            continue
        
        # Get feedback and display it
        feedback = get_feedback(secret_word, guess)
        guesses_history.append(" ".join(feedback))
        
        # Display the history of guesses
        for line in guesses_history:
            print(line)
        
        if guess == secret_word:
            print(f"\nCongratulations! You guessed the word '{secret_word}' in {attempts + 1} attempts!\n")
            return
            
        attempts += 1
        print()

    print(f"\nGame over! You've run out of attempts. The secret word was '{secret_word}'.\n")

if __name__ == "__main__":
    play_wordle()
