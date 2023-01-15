import os
from functools import lru_cache

from biblenlp.interface.models import Bible
from biblenlp.parsing.parse_structured import parse_from_xml_str_bible
from biblenlp.parsing.structure_xml import load_raw_structure_from


@lru_cache
def get_bible(filename: str) -> Bible:
    """Loads the Bible object from the specified XML file."""
    # Check if the file exists
    json_filename = f'{filename.split(".")[0]}.json'
    has_json = os.path.isfile(json_filename)
    if has_json:
        bible = Bible.parse_file(json_filename)
    else:
        raw_structure = load_raw_structure_from(filename=filename)
        bible = parse_from_xml_str_bible(raw_structure)
        bible.save(json_filename)
    return bible
