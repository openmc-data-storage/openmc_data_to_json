import os
from pathlib import Path


def test_extraction_of_cross_section():

    os.system("rm *.json")

    os.system("openmc-data-to-json -i tests/Be9.h5 -r n,2n -o my_reaction.json")

    assert Path("my_reaction.json").exists

def test_extraction_of_cross_section_with_brackets():

    os.system("rm *.json")

    os.system("openmc-data-to-json -i tests/Be9.h5 -r (n,2n) -o my_reaction.json")

    assert Path("my_reaction.json").exists

def test_extraction_of_cross_section_using_mt_number():

    os.system("rm *.json")

    os.system("openmc-data-to-json -i tests/Be9.h5 -r 16 -o my_reaction.json")

    assert Path("my_reaction.json").exists

def test_extraction_of_missing_cross_section():

    # should raise ValueError as reaction does not exist

    os.system("rm my_reaction.json")

    os.system("openmc-data-to-json -i tests/Be9.h5 -r n,f -o my_reaction.json")

    assert Path("my_reaction.json").exists() is False
