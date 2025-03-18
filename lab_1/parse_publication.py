import re
from typing import Optional


def parse_publication(reference: str) -> Optional[dict]:
    """
    Parse academic publication reference and extract structured information.

    Expected reference format:
    Lastname, I., Lastname2, I2. (Year). Title. Journal, Volume(Issue), StartPage-EndPage.

    Example:
    Kowalski, J., Nowak, A. (2023). Analiza algorytmów tekstowych. Journal of Computer Science, 45(2), 123-145.

    Args:
        reference (str): Publication reference string

    Returns:
        Optional[dict]: A dictionary containing parsed publication data or None if the reference doesn't match expected format
    """
    # Implement regex patterns to match different parts of the reference
    authors_year_pattern = r"(?P<authors>.*?) \((?P<year>\d{4})\)\."
    title_journal_pattern = r" (?P<title>.+?)\. (?P<journal>.+?),"
    volume_issue_pages_pattern = r" (?P<volume>\d+)(\((?P<issue>\d+)\))?, (?P<start_page>\d+)-(?P<end_page>\d+)\."

    # Combine the patterns
    full_pattern = rf"{authors_year_pattern}{title_journal_pattern}{volume_issue_pages_pattern}"

    # Use re.match to try to match the full pattern against the reference
    # If there's no match, return None
    match = re.match(full_pattern, reference)
    if not match:
        return None

    # Extract information using regex
    # Each author should be parsed into a dictionary with 'last_name' and 'initial' keys
    authors_list = []
    author_pattern = r"(?P<last_name>\w+), (?P<initial>\w)\."

    # Use re.finditer to find all authors and add them to authors_list
    authors = match.group("authors")
    for author_match in re.finditer(author_pattern, authors):
        authors_list.append({
            "last_name": author_match.group("last_name"),
            "initial": author_match.group("initial")
        })

    # Create and return the final result dictionary with all the parsed information
    # It should include authors, year, title, journal, volume, issue, and pages
    result = {
        "authors": authors_list,
        "year": int(match.group("year")),
        "title": match.group("title"),
        "journal": match.group("journal"),
        "volume": int(match.group("volume")),
        "issue": int(match.group("issue")) if match.group("issue") is not None else None,
        "pages": {
            "start": int(match.group("start_page")),
            "end": int(match.group("end_page"))
        }
    }

    return result
