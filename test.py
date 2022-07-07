from restructuring import Bible




def load_bible(path: str) -> Bible:
    """
    Loads a bible from a file.
    """

    return Bible.parse_file(path)

if __name__ == "__main__":
    bible = load_bible('restructuring/bible.json')