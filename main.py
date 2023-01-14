from biblenlp.parsing import load_raw_structure_from
from biblenlp.parsing import parse_from_xml_str_bible as parse_bible

raw_bible = load_raw_structure_from(filename='kjvfull.xml')
pybible = parse_bible(raw_bible)

with open('.bib.json', 'w+') as json_file:
    json_file.write(pybible.json(indent=0, exclude_unset=True))
