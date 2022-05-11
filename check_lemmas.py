# check_lemmas.py

"""Make sure all the lemmas in this project follow the right model"""

# Copyright 2022 Sustainable Sardinia
import json


def _check_string(element):
    assert isinstance(element, str), "Element should be a string but isn't."


def _check_string_or_list_of_strings(element):
    assert isinstance(element, str) or (
        isinstance(element, list) and all(isinstance(el, str) for el in element)
    ), "Element should be a string but isn't."


def _check_single_italian(italian_lemma: dict):
    keys = italian_lemma.keys()

    assert "lemma" in keys and "type" in keys, "Bad structure of italian lemma"
    _check_string(italian_lemma["lemma"])
    _check_string(italian_lemma["type"])


def _check_single_sardinian(sardinian_lemma: dict):
    keys = sardinian_lemma.keys()

    assert "type" in keys, "Sardinian lemma has no type"
    _check_string(sardinian_lemma["type"])

    if "campidanese" in keys and "logudorese" in keys:
        _check_string(sardinian_lemma["campidanese"])
        _check_string(sardinian_lemma["logudorese"])
    elif "both" in keys:
        _check_string(sardinian_lemma["both"])
    else:
        assert False, "Bad structure of sardinian lemma"

    assert "usage" in keys, "Sardinian lemma has no usage"
    _check_string(sardinian_lemma["usage"])


def _check_list_or_single(element, checker):
    if isinstance(element, list):
        for sub_element in element:
            checker(sub_element)
    elif isinstance(element, dict):
        checker(element)
    else:
        assert False, "Bad content for this entry"


def _check_single_foreign_language(foreign_lemma):
    _check_string_or_list_of_strings(foreign_lemma)


def _check_foreign_languages(entry: dict, foreign_languages: list):
    keys = entry.keys()

    for language in foreign_languages:
        assert language in keys, f"{language} entry is missing"
        _check_single_foreign_language(entry[language])


def _check_entry(entry: dict):
    keys = entry.keys()

    assert "italian" in keys, "Italian entry is missing"
    _check_list_or_single(entry["italian"], _check_single_italian)

    assert "discipline" in keys, "Discipline is missing"
    _check_string_or_list_of_strings(entry["discipline"])

    assert "description" in keys, "Description is missing"
    _check_string(entry["description"])

    assert "sardinian" in keys, "Sardinian entry is missing"
    _check_list_or_single(entry["sardinian"], _check_single_sardinian)

    _check_foreign_languages(
        entry, ["english", "german", "castillan", "catalan", "portuguese", "french"]
    )


if __name__ == "__main__":
    with open("lemariu.json", "r") as file:
        all_entries = json.load(file)

    for current_entry in all_entries:
        try:
            _check_entry(current_entry)
            print(f"Entry is valid: '{current_entry['description']}'")
        except Exception as cause:
            print("Entry is invalid")
            raise Exception("Bad entry") from cause
