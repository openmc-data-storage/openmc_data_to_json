
import os
import unittest
from pathlib import Path

from openmc_data_to_json import (cross_section_h5_file_to_json_files,
                                 cross_section_h5_files_to_json_files,
                                 cross_section_h5_to_json, reactions_in_h5)


class TestApiUsage(unittest.TestCase):

    def test_cross_section_h5_file_to_json_files(self):

        os.system('rm *.json')

        cross_section_h5_file_to_json_files(
            input='Li6.h5',
            output='tritium_production.json',
            reaction='(n,Xt)'
        )

        assert Path('tritium_production.json').exists

    def test_cross_section_h5_to_json(self):

        energy, xs = cross_section_h5_to_json(
            input='Li6.h5',
            output='tritium_production.json',
            reaction='(n,Xt)'
        )

        assert len(energy) == len(xs)

        for entry in energy:
            assert isinstance(entry, float)
        for entry in xs:
            assert isinstance(xs, float)

    def test_reactions_in_h5(self):

        reactions, mt_numbers = reactions_in_h5(input='Li6.h5')

        assert isinstance(reactions, list)
        assert '(n,Xt)' in reactions
        assert 205 in mt_numbers
        assert len(reactions) == len(mt_numbers)


if __name__ == "__main__":
    unittest.main()
