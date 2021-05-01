
import h5py
import openmc


def cross_section_from_h5_to_file():
    pass

def openmc_data_to_json():
    pass

def reactions_in_h5():
    pass

def open_h5(filename):

    with h5py.File(filename) as h5file:
        filetype = h5file.attrs['filetype'].decode()[5:] #same method as library.py

    if filetype == 'neutron':
        incident_particle_symbol = 'n'
        isotope_object = openmc.data.IncidentNeutron.from_hdf5(os.path.join(datapath, file))
    if filetype == 'photon':
        incident_particle_symbol = 'p'
        isotope_object = openmc.data.IncidentPhoton.from_hdf5(os.path.join(datapath, file))

    return isotope_object, 