import re


def extract_links(html: str) -> list[dict[str, str]]:
    """
    Extract all links from the given HTML string.

    Args:
        html (str): HTML content to analyze

    Returns:
        list[dict]: A list of dictionaries where each dictionary contains:
            - 'url': the href attribute value
            - 'title': the title attribute value (or None if not present)
            - 'text': the text between <a> and </a> tags
    """

    # TODO: Implement a regular expression pattern to extract links from HTML.
    # The pattern should capture three groups:
    # 1. The URL (href attribute value)
    # 2. The title attribute (which might not exist)
    # 3. The link text (content between <a> and </a> tags)
    url_pattern = r"href=\"(?P<url>).*?\""
    title_pattern = r"title=\"(?P<title>).*?\""
    pattern = r"<a(?P<flags>.*?)>(?P<text>).*?</a>"

    for line in html.splitlines():
        match = re.match(pattern, line)

        if not match:
            continue

        links = [link_match.group("url") for link_match in re.finditer(url_pattern, match.group("flags"))]

        # TODO: Use re.finditer to find all matches of the pattern in the HTML
        # For each match, extract the necessary information and create a dictionary
        # Then append that dictionary to the 'links' list

    print(links)

    return links
