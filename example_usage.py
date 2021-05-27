
from openmc_data_to_json import (cross_section_h5_file_to_json_files,
                                 cross_section_h5_files_to_json_files,
                                 cross_section_h5_to_json, reactions_in_h5)

# a= openmc_h5_to_json('/home/jshim/data/tendl-2019-hdf5/Li6.h5')

# for k,v in a.items():
#     print(k)

# print(a['Li_6__n_2_294K'].keys())

test_filename_1 = '/home/jshim/data/tendl-2019-hdf5/Li6.h5'
test_filename_2 = '/home/jshim/data/tendl-2019-hdf5/Li7.h5'

reactions = reactions_in_h5(test_filename_1)

filenames = cross_section_h5_file_to_json_files(test_filename_1)

filenames = cross_section_h5_files_to_json_files(
    filenames=[test_filename_1, test_filename_2],
    index_filename='index.json'
)

# list(pathlib.Path('your_directory').glob('*.txt'))
