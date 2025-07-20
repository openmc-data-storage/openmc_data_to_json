

import openmc_data_to_json as odj


test_filename_1 = '~/nuclear_data/Li6.h5'
test_filename_2 = '~/nuclear_data/Li7.h5'

reactions = odj.reactions_in_h5(test_filename_1)

filenames = odj.cross_section_h5_file_to_json_files(test_filename_1)

filenames = odj.cross_section_h5_files_to_json_files(
    filenames=[test_filename_1, test_filename_2],
    index_filename='index.json'
)

filename = odj.cross_section_h5_files_to_json_file(
    filenames=[test_filename_1, test_filename_2]
)

filename = odj.cross_section_h5_file_to_json_file(
    filename=test_filename_1
)


odj.extract_cross_section_data(h5_filename='tests/Li6.h5', json_filename='li6_neutron.json')
odj.extract_cross_section_data(h5_filename='tests/Li7.h5', json_filename='li7_neutron.json')
