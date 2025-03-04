def is_palindrome(text: str):
    # Remove spaces and convert the text to lowercase
    text = "".join(filter(lambda char: char != ' ', text)).lower()

    # Check if the text read from the front is the same as from the back
    # HINT: Use the notation text[::-1] to reverse the text
    return text == text[::-1]

def make_palindrome(text: str):
    # Remove spaces and convert to lowercase
    text = text.lower().replace(" ", "")

    # Check if it is already a palindrome
    if is_palindrome(text):
        return text

    # Create a palindrome by adding reversed characters at the end
    # (excluding the last character, which is already at the start of the reversed text)
    option1 = text + text[-1::-1]

    # Create a palindrome by adding reversed characters at the beginning
    # (excluding the first character, which is already at the end of the original text)
    option2 = text[1:] + text

    # Return the shorter option as the result
    return option1 if len(option1) < len(option2) else option2

def palindrome_checker():
    # Retrieve data from the user
    text = input("Enter a word or phrase: ")

    # Remove characters that are not letters or numbers, and convert to lowercase
    # HINT: Use the isalnum() function and list comprehension or a generator expression
    clean_text = "".join([char for char in text if char.isalnum()])

    # Check if it is a palindrome
    if is_palindrome(clean_text):
        print(f"\"{text}\" is a palindrome!")
    else:
        print(f"\"{text}\" is not a palindrome.")
        suggested = make_palindrome(clean_text)
        print(f"Suggested palindrome: {suggested}")

# Call the function
if __name__ == "__main__":
    palindrome_checker()
