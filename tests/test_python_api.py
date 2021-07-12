
import os
import unittest
from pathlib import Path

from openmc_data_to_json import (cross_section_h5_file_to_json_files,
                                 cross_section_h5_files_to_json_files,
                                 cross_section_h5_file_to_json_file,
                                 cross_section_h5_to_json, reactions_in_h5)


class TestApiUsage(unittest.TestCase):

    def test_cross_section_h5_file_to_json_files(self):

        os.system('rm *.json')

        cross_section_h5_file_to_json_file(
            filename='tests/Li6.h5',
            output='tritium_production.json',
            reaction='(n,Xt)'
        )

        assert Path('tritium_production.json').exists


    def test_for_trailing_zeros(self):


        list_of_reactions = cross_section_h5_to_json(
                filename='tests/FENDL-3.1d_Ag109.h5',
                reaction='all'
            )
        for entry in list_of_reactions: 
            xs = entry['cross section']
            print(xs)
            assert xs[-1] != 0

    def test_cross_section_h5_to_json(self):


        for isotope, reaction in zip(['Be9.h5', 'Li6.h5', 'Li7.h5'], ['(n,Xt)', '(n,Xt)', '(n,Xt)']):
            dict_of_reactions = cross_section_h5_to_json(
                filename='tests/'+isotope,
                reaction=reaction
            )

            energy = dict_of_reactions[0]['energy']
            xs = dict_of_reactions[0]['cross section']

            assert len(energy) == len(xs)

            for entry in energy:
                assert isinstance(entry, float)
            for entry in xs:
                assert isinstance(entry, float)
            assert xs[-1] != 0

    def test_reactions_in_h5(self):

        reactions = reactions_in_h5(filename='tests/Li6.h5')

        assert isinstance(reactions, list)
        assert '(n,Xt)' in reactions
        # assert 205 in mt_numbers
        # assert len(reactions) == len(mt_numbers)


if __name__ == "__main__":
    unittest.main()
