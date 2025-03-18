import re
from collections import Counter


def analyze_text_file(filename: str) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        return {"error": f"Could not read file: {str(e)}"}

    # Common English stop words to filter out from frequency analysis
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "with",
        "by",
        "about",
        "as",
        "into",
        "like",
        "through",
        "after",
        "over",
        "between",
        "out",
        "of",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "from",
        "there",
        "their",
    }

    # Implement word extraction using regex
    # Find all words in the content (lowercase for consistency)
    word_pattern = r"\b\w+\b"

    words = re.findall(word_pattern, content)
    # words = list(filter(lambda word: word not in stop_words, words))
    word_count = len(words)

    # Implement sentence splitting using regex
    # A sentence typically ends with ., !, or ? followed by a space
    # Be careful about abbreviations (e.g., "Dr.", "U.S.A.")
    sentence_pattern = r"[^.!?]+[.!?]"
    sentences = re.findall(sentence_pattern, content)
    sentence_count = len([s for s in sentences if s.strip()])

    # Implement email extraction using regex
    # Extract all valid email addresses from the content
    # email_pattern = r"(\S+?\.){0,}\S+?@(.+?\.){1,}.+?"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, content)

    # Calculate word frequencies
    # Count occurrences of each word, excluding stop words and short words
    # Use the Counter class from collections
    word_counter = Counter(
        filter(
            lambda word: len(word) > 2 and word not in stop_words,
            re.findall(word_pattern, content))
        )
    frequent_words = Counter(dict(word_counter.most_common(10)))

    # Implement date extraction with multiple formats
    # Detect dates in various formats: YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY, etc.
    # Create multiple regex patterns for different date formats
    date_patterns = [r"\d{4}([-./]\d{2}){2}",
                     r"(\d{2}[-./]){2}\d{4}",
                     r"\w+ \d{1,2}, \d{1,4}"]


    date_pattern = re.compile("(" + ")|(".join(date_patterns) + ")")
    dates = [match.group() for match in re.finditer(date_pattern, content)]

    # Analyze paragraphs
    # Split the content into paragraphs and count words in each
    # Paragraphs are typically separated by one or more blank lines
    paragraphs = re.split(r"\n\s*\n", content)

    paragraph_sizes = {}

    for no, paragraph in enumerate(paragraphs):
        words = re.findall(word_pattern, paragraph)
        paragraph_sizes[no] = len(words)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "emails": emails,
        "frequent_words": frequent_words,
        "dates": dates,
        "paragraph_sizes": paragraph_sizes,
    }
