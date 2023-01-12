from biblenlp.restructuring import untangle_osis
from biblenlp.restructuring import parse_from_xml_str_bible as parse_bible


if __name__ == "__main__":
    from devtools import debug
    original = input("Path to the original XML: ")
    filename = input("Path for the new file: ")
    raw_bible = untangle_osis(original)
    pybible = parse_bible(raw_bible)  # type: ignore
