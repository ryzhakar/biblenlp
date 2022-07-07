from restructuring import Bible, Corpus, Word


def bible_fr_json(path: str) -> Bible:
    """
    Loads a bible from a file.
    """

    return Bible.parse_file(path)

def get_subcorpus(parent: Corpus, child_name: str) -> Corpus:
    if isinstance(parent, Word):
        raise TypeError("Can't get a subcorpus from a word.")
    
    return parent.as_dict().get(child_name)  # type: ignore

if __name__ == "__main__":
    bible = bible_fr_json('restructuring/bible.json')