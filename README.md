
This is a minimal Python package that provides both command line and API 
interfaces for converting OpenMC h5 nuclear data files into JSON files for each
reaction.

This is useful for building a nuclear data database where JSON files are
commonly accepted inputs. This tool is used for the generation of the
[xsplot.com](http:/www.xsplot.com) database.


# Python API usage

Extracting a single reaction from the h5 file using the API

```python
from openmc_data_to_json import reaction_from_h5_to_json_file

reaction_from_h5_to_json_file(
    input='Li6.h5',
    output='tritium_production.json',
    reaction='(n,Xt)'
)
```

There are other API functions that might be of interest like 
```reaction_from_h5_to_json```, ```reaction_from_h5``` and ```reaction_in_h5```

# Command line usage

Another use of this program is to extract reactions using the command line tool.

```bash
openmc-data-to-json -i Be9.h5 -r (n,2n) -o my_reaction.json
```

- the ```-i``` or ```--input``` argument specifies the input h5 file
- the ```-o``` or ```--output``` argument specifies the output json filename
- the ```-r``` or ```--reaction``` argument specifies the reactions to extract.

# Installation

The easiest way to install is to use the PyPi distribution.

```bash
pip install openmc_data_to_json
```
