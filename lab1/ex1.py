def text_counter():
    # Retrieving data from the user
    text = input("Enter the text to analyze: ")

    ### Calculations ###

    # Calculate the total number of characters in the text
    char_count = len(text)

    # Calculate the number of characters without spaces
    char_count_no_spaces = sum(1 for char in text if char != ' ')

    # Split the text into words and count them
    words = text.split()
    word_count = len(words)

    # Counting vowels and consonants
    vowels = "aeiouAEIOUąęióóyĄĘIÓÓY"
    consonants = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZćłńśźżĆŁŃŚŹŻ"

    # Count the vowels in the text
    vowel_count = sum(1 for char in text if char in vowels)

    # Count the consonants in the text
    consonant_count = sum(1 for char in text if char in consonants)

    # Displaying results
    print(f"\nText analysis: \"{text}\"")
    print(f"Number of words: {word_count}")
    print(f"Number of characters (with spaces): {char_count}")
    print(f"Number of characters (without spaces): {char_count_no_spaces}")
    print(f"Number of vowels: {vowel_count}")
    print(f"Number of consonants: {consonant_count}")

# Call the function
if __name__ == "__main__":
    text_counter()
