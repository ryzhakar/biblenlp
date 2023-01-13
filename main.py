from biblenlp.restructuring import parse_from_xml_str_bible as parse_bible
from biblenlp.restructuring import untangle_osis


raw_bible = untangle_osis('kjvfull.xml')
pybible = parse_bible(raw_bible)  # type: ignore

with open('.bib.json', 'w+') as json_file:
    json_file.write(pybible.json(indent=0, exclude_unset=True))
