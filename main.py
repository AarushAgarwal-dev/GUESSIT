import random

# Functions for Movie Guessing Game
class Settings:
    wrong_guesses_allowed = 6

class WordList:
    all_movies = [
        "Sholay", "Dilwale Dulhania Le Jayenge", "Mughal-e-Azam", "3 Idiots", "Lagaan", "Dangal",
        "Gully Boy", "Kabhi Khushi Kabhie Gham", "PK", "Andaz Apna Apna", "Swades", "Chak De! India",
        "Koi Mil Gaya", "Queen", "Drishyam", "Baahubali: The Beginning", "Haider", "Jab Tak Hai Jaan",
        "Devdas", "Rang De Basanti", "The Godfather", "Shawshank Redemption", "Pulp Fiction",
        "The Dark Knight", "Forrest Gump", "Inception", "Titanic", "The Matrix", "Avatar",
        "Jurassic Park"
    ]

    @staticmethod
    def get_random_word():
        return random.choice(WordList.all_movies)

class Session:
    def __init__(self):
        self.word = WordList.get_random_word()
        self.remaining_wrong_guesses = Settings.wrong_guesses_allowed
        self.letter_guessed = [False] * 26

    def to_index(self, c):
        return ord(c) % 32 - 1

    def get_word(self):
        return self.word

    def get_remaining_wrong_guesses(self):
        return self.remaining_wrong_guesses

    def remove_guess(self):
        self.remaining_wrong_guesses -= 1

    def is_letter_guessed(self, c):
        return self.letter_guessed[self.to_index(c)]

    def set_letter_guessed(self, c):
        self.letter_guessed[self.to_index(c)] = True

    def is_letter_in_word(self, c):
        return c.lower() in self.word.lower()

    def won(self):
        return all(self.is_letter_guessed(c) for c in self.word)

def draw(s):
    print("\n")
    print("The movie: ", end="")
    for c in s.get_word():
        if c.isalpha() and s.is_letter_guessed(c.upper()):
            print(c, end="")
        elif c.isspace():
            print(" ", end="")
        else:
            print('_', end="")

    print("   Wrong guesses: " + '+' * s.get_remaining_wrong_guesses())

    for c in 'abcdefghijklmnopqrstuvwxyz':
        if s.is_letter_guessed(c.upper()) and not s.is_letter_in_word(c.upper()):
            print(c, end="")
        elif s.is_letter_guessed(c.lower()) and not s.is_letter_in_word(c.lower()):
            print(c, end="")

    print('\n')

def get_guess(s):
    while True:
        c = input("Enter your next letter: ")

        if not c.isalpha() or len(c) != 1:
            print("That wasn't a valid input. Try again.")
            continue

        c = c.lower()

        if s.is_letter_guessed(c):
            print("You already guessed that. Try again.")
            continue

        return c

def handle_guess(s, c):
    s.set_letter_guessed(c)

    if s.is_letter_in_word(c):
        print(f"Yes, '{c}' is in the movie!")
    else:
        print(f"No, '{c}' is not in the movie!")
        s.remove_guess()

# Functions for Number Guessing Game
def get_digits(num):
    return [int(i) for i in str(num)]

def no_duplicates(num):
    num_list = get_digits(num)
    return len(num_list) == len(set(num_list))

def generate_num():
    while True:
        num = random.randint(1000, 9999)
        if no_duplicates(num):
            return num

def num_of_cdcp_cdwp(num, guess):
    cdcp_cdwp = [0, 0]
    num_list = get_digits(num)
    guess_list = get_digits(guess)

    for i, j in zip(num_list, guess_list):
        if j in num_list:
            if j == i:
                cdcp_cdwp[0] += 1
            else:
                cdcp_cdwp[1] += 1

    return cdcp_cdwp

# Main Game
print("Welcome to the Guessing Game!")
print("Choose a game:")
print("1. Guess the movie")
print("2. Guess the number")

choice = input("Enter 1 or 2: ")

if choice == "1":
    session = Session()

    while session.get_remaining_wrong_guesses() and not session.won():
        draw(session)
        guess = get_guess(session)
        handle_guess(session, guess)

    draw(session)

    if not session.get_remaining_wrong_guesses():
        print("You lost! The word was:", session.get_word())
    else:
        print("You won!")

elif choice == "2":
    secret_num = generate_num()
    tries = int(input('Enter number of tries: '))

    while tries > 0:
        guess = int(input("Enter your guess: "))

        if not no_duplicates(guess):
            print("Number should not have repeated digits. Try again.")
            continue
        if guess < 1000 or guess > 9999:
            print("Enter a 4-digit number only. Try again.")
            continue

        cdcp_cdwp = num_of_cdcp_cdwp(secret_num, guess)
        print(f"{cdcp_cdwp[0]} correct digits in the correct position, {cdcp_cdwp[1]} correct digits in the wrong position.")
        tries -= 1

        if cdcp_cdwp[0] == 4:
            print("You guessed right!")
            break
    else:
        print(f"You ran out of tries. The number was {secret_num}")

else:
    print("Invalid choice. Please enter 1 or 2.")
