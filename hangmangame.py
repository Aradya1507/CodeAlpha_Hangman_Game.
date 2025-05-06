import streamlit as st
import random

# A larger list of words and their corresponding clues
word_clues = {
    "python": "A popular programming language known for its readability.",
    "hangman": "A game where you guess letters to reveal a hidden word.",
    "streamlit": "A framework for building web apps for data science.",
    "development": "The process of creating software applications.",
    "artificial": "Relating to human-made systems or processes.",
    "intelligence": "The ability to acquire and apply knowledge and skills.",
    "programming": "The process of writing computer programs.",
    "data": "Facts and statistics collected for reference or analysis.",
    "science": "A systematic enterprise that builds and organizes knowledge.",
    "machine": "A device that uses power to perform a specific task.",
    "algorithm": "A step-by-step procedure for calculations.",
    "database": "An organized collection of data.",
    "software": "The programs and other operating information used by a computer.",
    "hardware": "The physical parts of a computer.",
    "network": "A group of interconnected computers.",
    "cloud": "A system of remote servers hosted on the Internet.",
    "cybersecurity": "The practice of protecting systems from digital attacks.",
    "machine learning": "A subset of AI that enables systems to learn from data.",
    "blockchain": "A system in which records are maintained across several computers.",
    "virtualization": "The creation of a virtual version of something.",
    "internet": "A global network connecting millions of private, public, academic, business, and government networks."
}

# Function to select a random word and its clue
def get_random_word_and_clue(used_words):
    available_words = {word: clue for word, clue in word_clues.items() if word not in used_words}
    if not available_words:
        return None, None  # No more words available
    word = random.choice(list(available_words.keys()))
    clue = available_words[word]
    return word, clue

# Function to display the current state of the word
def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# Main function to run the game
def main():
    st.set_page_config(page_title="Hangman Game", page_icon="🎮", layout="centered")
    st.title("🎮 Hangman Game 🎮")
    st.write("Guess the word by entering one letter at a time!")

    # Initialize session state
    if 'used_words' not in st.session_state:
        st.session_state.used_words = set()
        st.session_state.word, st.session_state.clue = get_random_word_and_clue(st.session_state.used_words)
        st.session_state.guessed_letters = set()
        st.session_state.incorrect_guesses = 0
        st.session_state.max_incorrect_guesses = 6

    # Check if there are no more words available
    if st.session_state.word is None:
        st.warning("No more unique words available! Please restart the game.")
        if st.button("Restart Game"):
            st.session_state.clear()
        return

    # Display the clue
    st.markdown(f"<h4 style='text-align: center;'>Clue: {st.session_state.clue}</h4>", unsafe_allow_html=True)

    # Display the current state of the word
    current_word_display = display_word(st.session_state.word, st.session_state.guessed_letters)
    st.markdown(f"<h2 style='text-align: center;'>{current_word_display}</h2>", unsafe_allow_html=True)

    # Display the number of incorrect guesses left
    st.markdown(f"<h4 style='text-align: center;'>Incorrect guesses left: {st.session_state.max_incorrect_guesses - st.session_state.incorrect_guesses}</h4>", unsafe_allow_html=True)

    # Input for guessing a letter
    guess = st.text_input("Enter a letter:", max_chars=1).lower()

    if st.button("Submit Guess"):
        if guess and guess not in st.session_state.guessed_letters:
            st.session_state.guessed_letters.add(guess)

            if guess not in st.session_state.word:
                st.session_state.incorrect_guesses += 1
                st.error(f"Wrong guess! '{guess}' is not in the word.")
            else:
                st.success(f"Good guess! '{guess}' is in the word.")

        # Check for win or loss
        if all(letter in st.session_state.guessed_letters for letter in st.session_state.word):
            st.success(f"🎉 Congratulations! You've guessed the word: **{st.session_state.word}** 🎉")
            st.session_state.used_words.add(st.session_state.word)  # Add the word to used words
            st.session_state.word, st.session_state.clue = get_random_word_and_clue(st.session_state.used_words)  # Get a new word
            st.session_state.guessed_letters.clear()  # Clear guessed letters
            st.session_state.incorrect_guesses = 0  # Reset incorrect guesses
        elif st.session_state.incorrect_guesses >= st.session_state.max_incorrect_guesses:
            st.error(f"Game over! The word was: **{st.session_state.word}**")
            st.session_state.used_words.add(st.session_state.word)  # Add the word to used words
            st.session_state.word, st.session_state.clue = get_random_word_and_clue(st.session_state.used_words)  # Get a new word
            st.session_state.guessed_letters.clear()  # Clear guessed letters
            st.session_state.incorrect_guesses = 0  # Reset incorrect guesses

    # Option to restart the game
    if st.button("Restart Game"):
        st.session_state.clear()

    # Add some styling
    st.markdown("""
        <style>
        .stTextInput>div>input {
            font-size: 24px;
            text-align: center;
        }
        .stButton>button {
            font-size: 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()