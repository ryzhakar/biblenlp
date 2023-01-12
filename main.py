from biblenlp.restructuring import untangle_osis
from biblenlp.restructuring import parse_from_xml_str_bible as parse_bible


if __name__ == "__main__":
    from devtools import debug
    raw_bible = untangle_osis("kjvfull.xml")
    pybible = parse_bible(raw_bible)  # type: ignore
    
    with open('.bib.json', 'w+') as f:
        f.write(pybible.json(indent=0, exclude_unset=True))
