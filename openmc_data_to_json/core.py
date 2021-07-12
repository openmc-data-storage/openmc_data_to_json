
import json
from pathlib import Path 


import h5py
import numpy as np
import openmc
from typing import Optional, List

ELEMENT_NAME = {
    0: 'neutron', 1: 'Hydrogen', 2: 'Helium', 3: 'Lithium',
    4: 'Beryllium', 5: 'Boron', 6: 'Carbon', 7: 'Nitrogen',
    8: 'Oxygen', 9: 'Fluorine', 10: 'Neon', 11: 'Sodium',
    12: 'Magnesium', 13: 'Aluminium', 14: 'Silicon',
    15: 'Phosphorus', 16: 'Sulfur', 17: 'Chlorine',
    18: 'Argon', 19: 'Potassium', 20: 'Calcium',
    21: 'Scandium', 22: 'Titanium', 23: 'Vanadium',
    24: 'Chromium', 25: 'Manganese', 26: 'Iron',
    27: 'Cobalt', 28: 'Nickel', 29: 'Copper', 30: 'Zinc',
    31: 'Gallium', 32: 'Germanium', 33: 'Arsenic',
    34: 'Selenium', 35: 'Bromine', 36: 'Krypton',
    37: 'Rubidium', 38: 'Strontium', 39: 'Yttrium',
    40: 'Zirconium', 41: 'Niobium', 42: 'Molybdenum',
    43: 'Technetium', 44: 'Ruthenium', 45: 'Rhodium',
    46: 'Palladium', 47: 'Silver', 48: 'Cadmium', 49: 'Indium',
    50: 'Tin', 51: 'Antimony', 52: 'Tellurium', 53: 'Iodine',
    54: 'Xenon', 55: 'Caesium', 56: 'Barium', 57: 'Lanthanum',
    58: 'Cerium', 59: 'Praseodymium', 60: 'Neodymium',
    61: 'Promethium', 62: 'Samarium', 63: 'Europium', 
    64: 'Gadolinium', 65: 'Terbium', 66: 'Dysprosium',
    67: 'Holmium', 68: 'Erbium', 69: 'Thulium',
    70: 'Ytterbium', 71: 'Lutetium', 72: 'Hafnium',
    73: 'Tantalum', 74: 'Tungsten', 75: 'Rhenium',
    76: 'Osmium', 77: 'Iridium', 78: 'Platinum',
    79: 'Gold', 80: 'Mercury', 81: 'Thallium',
    82: 'Lead', 83: 'Bismuth', 84: 'Polonium',
    85: 'Astatine', 86: 'Radon', 87: 'Francium',
    88: 'Radium', 89: 'Actinium', 90: 'Thorium',
    91: 'Protactinium', 92: 'Uranium', 93: 'Neptunium',
    94: 'Plutonium', 95: 'Americium', 96: 'Curium',
    97: 'Berkelium', 98: 'Californium', 99: 'Einsteinium',
    100: 'Fermium', 101: 'Mendelevium', 102: 'Nobelium',
    103: 'Lawrencium', 104: 'Rutherfordium', 105: 'Dubnium',
    106: 'Seaborgium', 107: 'Bohrium', 108: 'Hassium',
    109: 'Meitnerium', 110: 'Darmstadtium', 111: 'Roentgenium',
    112: 'Copernicium', 113: 'Nihonium', 114: 'Flerovium',
    115: 'Moscovium', 116: 'Livermorium', 117: 'Tennessine',
    118: 'Oganesson'
}

# for reaction in REACTION_NAME: 
#     REACTION_NAME[reaction] = REACTION_NAME[reaction][3:-1]
def make_REACTION_DICT():

    REACTION_NAME = {
        1: 'total', 
        2: 'elastic', 
        4: 'level',
        5: 'misc', 
        11: '2nd', 
        16: '2n', 
        17: '3n',
        18: 'fission', 
        19: 'f', 
        20: 'nf', 
        21: '2nf',
        22: 'na', 
        23: 'n3a', 
        24: '2na', 
        25: '3na',
        27: 'absorption', 
        28: 'np', 
        29: 'n2a',
        30: '2n2a', 
        32: 'nd', 
        33: 'nt', 
        34: 'nHe-3',
        35: 'nd2a', 
        36: 'nt2a', 
        37: '4n', 
        38: '3nf',
        41: '2np', 
        42: '3np', 
        44: 'n2p', 
        45: 'npa',
        91: 'nc', 
        101: 'disappear', 
        102: 'gamma',
        103: 'p', 
        104: 'd', 
        105: 't', 
        106: '3He',
        107: 'a', 
        108: '2a', 
        109: '3a', 
        111: '2p',
        112: 'pa', 
        113: 't2a', 
        114: 'd2a', 
        115: 'pd',
        116: 'pt', 
        117: 'da', 
        152: '5n', 
        153: '6n',
        154: '2nt', 
        155: 'ta', 
        156: '4np', 
        157: '3nd',
        158: 'nda', 
        159: '2npa', 
        160: '7n', 
        161: '8n',
        162: '5np', 
        163: '6np', 
        164: '7np', 
        165: '4na',
        166: '5na', 
        167: '6na', 
        168: '7na', 
        169: '4nd',
        170: '5nd', 
        171: '6nd', 
        172: '3nt', 
        173: '4nt',
        174: '5nt', 
        175: '6nt', 
        176: '2n3He',
        177: '3n3He', 
        178: '4n3He', 
        179: '3n2p',
        180: '3n3a', 
        181: '3npa', 
        182: 'dt',
        183: 'npd', 
        184: 'npt', 
        185: 'ndt',
        186: 'np3He', 
        187: 'nd3He', 
        188: 'nt3He',
        189: 'nta', 
        190: '2n2p', 
        191: 'p3He',
        192: 'd3He', 
        193: '3Hea', 
        194: '4n2p',
        195: '4n2a', 
        196: '4npa', 
        197: '3p',
        198: 'n3p', 
        199: '3n2pa', 
        200: '5n2p', 
        444: 'damage',
        649: 'pc', 
        699: 'dc', 
        749: 'tc', 
        799: '3Hec',
        849: 'ac', 
        891: '2nc'}

    REACTION_NAME.update({i: 'n{}'.format(i - 50) for i in range(50, 91)})
    REACTION_NAME.update({i: 'p{}'.format(i - 600) for i in range(600, 649)})
    REACTION_NAME.update({i: 'd{}'.format(i - 650) for i in range(650, 699)})
    REACTION_NAME.update({i: 't{}'.format(i - 700) for i in range(700, 749)})
    REACTION_NAME.update({i: '3He{}'.format(i - 750) for i in range(750, 799)})
    REACTION_NAME.update({i: 'a{}'.format(i - 800) for i in range(800, 849)})
    REACTION_NAME.update({i: '2n{}'.format(i - 875) for i in range(875, 891)})

    REACTION_NAME[3] = 'nonelastic'
    REACTION_NAME[203] = 'Xp'
    REACTION_NAME[204] = 'Xd'
    REACTION_NAME[205] = 'Xt'
    REACTION_NAME[206] = '3He'
    REACTION_NAME[207] = 'Xa'
    REACTION_NAME[301] = 'heat'
    REACTION_NAME[901] = 'displacement NRT'

    return REACTION_NAME


def find_REACTION_MT(val):
    for key, value in make_REACTION_DICT().items():
        if val == value or val.strip('(n,').strip(')') == value:
            return key
    raise ValueError(val, 'val not found in', make_REACTION_DICT().values())


def find_REACTION_NAME(keynumber, incident_particle_symbol='n'):

    REACTION_NAME = make_REACTION_DICT()

    for key, value in REACTION_NAME.items():
        REACTION_NAME[key] = '({},{})'.format(incident_particle_symbol, value)

    return REACTION_NAME[keynumber]


def find_REACTION_products(keynumber):

    return make_REACTION_DICT()[keynumber]


def cross_section_h5_files_to_json_files(
    filenames: List[str],
    output_dir: str = '',
    library: str = '',
    reaction: str = 'all',
    index_filename: str = None
):
    output_filenames = []
    index_dict = []
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        dict_of_reactions = cross_section_h5_to_json(
            filename=str(filename),
            library=library,
            reaction=reaction
        )
        # for key, value in dict_of_reactions.items():
        for entry in dict_of_reactions:
            output_filename = Path(output_dir)/Path(entry['uuid']+'.json')
            with open(output_filename, 'w') as fout:
                json.dump(entry, fout, indent=2)
            output_filenames.append(str(output_filename))

        if index_filename:
            # for key, value in dict_of_reactions.items():
            for entry in dict_of_reactions:
                del entry['cross section']
                del entry['energy']
                del entry['uuid']

            index_dict = index_dict + dict_of_reactions

            # output_filename = Path(filename).stem
            # output_filename = Path(output_filename).with_suffix('.json')
            # output_filename = Path(output_dir)/output_filename

    if index_filename:
        with open(Path(output_dir)/index_filename, 'w') as fout:
            json.dump(index_dict, fout, indent=2)
        output_filenames.append(str(index_filename))

    return output_filenames


def cross_section_h5_files_to_json_file(
    filenames,
    output='my_reactions.json',
    reaction='all',
    library=''
):

    list_of_reactions = []
    for filename in filenames:
        dict_of_reactions = cross_section_h5_to_json(
            filename=filename,
            library=library,
            reaction=reaction
        )
        list_of_reactions.append(dict_of_reactions)

    with open(output, 'w') as fout:
        json.dump(list_of_reactions, fout, indent = 2)

    return output


def cross_section_h5_file_to_json_files(
    filename: str,
    output_dir: str = '',
    library: str = '',
    index_filename: str = None,
    reaction='all'
):
    
    dict_of_reactions = cross_section_h5_to_json(
        filename=filename,
        library=library,
        reaction=reaction
    )

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_filenames = []
    for entry in dict_of_reactions:
        output_filename = Path(output_dir)/Path(entry['uuid']+'.json')
        with open(output_filename, 'w') as fout:
            json.dump(entry, fout, indent=2)
        output_filenames.append(str(output_filename))

    if index_filename:
        for entry in dict_of_reactions:
            del entry['cross section']
            del entry['energy']
        
        # output_filename = Path(filename).stem
        # output_filename = Path(output_filename).with_suffix('.json')
        # output_filename = Path(output_dir)/output_filename

        with open(Path(output_dir)/index_filename, 'w') as fout:
            json.dump(dict_of_reactions, fout, indent = 2)
        output_filenames.append(str(index_filename))
    
    return output_filenames


def cross_section_h5_file_to_json_file(
    filename,
    output='my_reactions.json',
    reaction='all',
    library=''
):
    dict_of_reactions = cross_section_h5_to_json(
        filename=filename,
        library=library,
        reaction=reaction
    )

    with open(output, 'w') as fout:
        json.dump(dict_of_reactions, fout, indent = 2)
    
    return output 

def cross_section_h5_to_json(
    filename: str,
    library='',
    reaction='all',
) -> dict:

    dict_of_reactions = []#{}
    isotope_object, particle = open_h5(filename)
    incident_particle_symbol = particle[0]
    
    if reaction == 'all':
        reactions = []
        for key, value in isotope_object.reactions.items():
            reactions.append(key)
        reactions.append('total')
    elif isinstance(reaction, (str, int)):
        reactions = [reaction]
    else:
        reactions = reaction
    
    reaction_mt_numbers = []
    for reaction in reactions:
        if isinstance(reaction, (int, np.integer, np.int64)):
            reaction_mt_numbers.append(reaction)
        elif isinstance(reaction, str) and reaction.isnumeric():
            reaction_mt_numbers.append(int(reaction))
        else:
            reaction_mt_numbers.append(find_REACTION_MT(reaction))
    
    for reaction in reaction_mt_numbers:

        if reaction not in [1] and reaction not in isotope_object.reactions:
            raise ValueError(reaction, ' not in avalaible reactions')
        temperatures = isotope_object[reaction].xs.keys()
        for temperature in temperatures:
            energy = isotope_object.energy[temperature]
            cross_section = isotope_object[reaction].xs[temperature](energy)

            shorter_cross_section = np.trim_zeros(cross_section, 'b')

            ofset = len(cross_section) - len(shorter_cross_section)

            shorter_energy= energy[ofset:]

            if int(isotope_object._mass_number)!=0: #this prevents natural (e.g. Carbon)

                neutron_number = int(isotope_object._mass_number-isotope_object._atomic_number)
                mass_number = int(isotope_object._mass_number)

                # print('creating json object for ',isotope_object.name, 'MT',reaction, temperature)

                reaction_dict = {
                    'Proton number':int(isotope_object._atomic_number),
                    'Mass number':mass_number,
                    'Neutron number':neutron_number,
                    'Element':ELEMENT_NAME[int(isotope_object._atomic_number)].lower(),
                    'Atomic symbol':isotope_object.atomic_symbol,
                    'Temperature(K)':temperature.replace('K', ''),
                    'Incident particle':'neutron',
                    'Reaction products':find_REACTION_products(int(reaction)),
                    'MT reaction number':int(reaction), # mt number
                    'Library':library,
                    'cross section':shorter_cross_section.tolist(),
                    'energy':shorter_energy.tolist(),
                    'uuid':'_'.join([isotope_object.atomic_symbol, str(mass_number), library, incident_particle_symbol, str(int(reaction)), str(temperature)])
                }

                # reaction_dict = {
                #     'Proton number / element':str(int(isotope_object._atomic_number)) +' '+isotope_object.atomic_symbol + ' '  + ELEMENT_NAME[int(isotope_object._atomic_number)],
                #     'Mass number':mass_number,
                #     'Neutron number':neutron_number,
                #     'MT number / reaction products':str(int(reaction)) + ' ' +find_REACTION_NAME(reaction, incident_particle_symbol),
                #     'Library':library,
                #     # 'Temperature':temperature,
                #     'cross section':shorter_cross_section.tolist(),
                #     'energy':shorter_energy.tolist(),
                #     'uuid':'_'.join([isotope_object.atomic_symbol, str(mass_number), library, incident_particle_symbol, str(int(reaction)), str(temperature)])
                # }

                # dict_of_reactions[uuid] = reaction_dict
                dict_of_reactions.append(reaction_dict)

    return dict_of_reactions


def reactions_in_h5(
    filename: str
):
    isotope_object, particle = open_h5(filename)
    reactions = []
    for key, value in isotope_object.reactions.items():
        reactions.append(find_REACTION_NAME(value.mt))
        # print(dir(value))
    return reactions


def open_h5(
    filename: str
):

    with h5py.File(filename) as h5file:
        # same method as openmc library.py
        particle = h5file.attrs['filetype'].decode()[5:]

    if particle == 'neutron':
        isotope_object = openmc.data.IncidentNeutron.from_hdf5(filename)
    if particle == 'photon':
        isotope_object = openmc.data.IncidentPhoton.from_hdf5(filename)

    return isotope_object, particle
