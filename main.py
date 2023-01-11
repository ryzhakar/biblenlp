from biblenlp.restructuring import untangle_osis
from biblenlp.restructuring import restructure_soup_bible


if __name__ == "__main__":
    original = input("Path to the original XML: ")
    filename = input("Path for the new file: ")
    bible = untangle_osis(original)
    pybible = restructure_soup_bible(bible) # type: ignore

    with open(filename, 'w+') as f:
        j = pybible.json(indent=0)
        f.write(j)


