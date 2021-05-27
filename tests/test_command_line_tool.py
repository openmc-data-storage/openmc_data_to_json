
import os
import unittest
from pathlib import Path


class TestUsage(unittest.TestCase):

    def test_extraction_of_cross_section(self):

        os.system('rm *.json')

        os.system("openmc-data-to-json -i tests/Be9.h5 -r n,2n -o my_reaction.json")

        assert Path('my_reaction.json').exists

    def test_extraction_of_cross_section_using_mt_number(self):

        os.system('rm *.json')

        os.system("openmc-data-to-json -i tests/Be9.h5 -r 16 -o my_reaction.json")

        assert Path('my_reaction.json').exists

    def test_extraction_of_missing_cross_section(self):

        os.system('rm *.json')

        os.system("openmc-data-to-json -i tests/Be9.h5 -r n,f -o my_reaction.json")

        assert Path('my_reaction.json').exists is False


if __name__ == "__main__":
    unittest.main()
