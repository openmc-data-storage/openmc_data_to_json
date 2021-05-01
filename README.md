
This is a minimal Python package that provides both command line and API 
interfaces for converting OpenMC h5 nuclear data files into JSON files for each
reaction.

This is useful for building a nuclear data database where JSON files are
commonly accepted inputs. This tool is used for the generation of the
[xsplot.com](http:/www.xsplot.com) database.


# Python API usage

Extracting a single reaction from the h5 file using the API and saving as a
CSV or JSON file.

```python
import openmc_data_to_json as odj

odj.cross_section_from_h5_to_file(
    input='Li6.h5',
    output='tritium_production.json',
    reaction='(n,Xt)',
    format='json'  # csv is also acceptable
)
```

It is also possible to return the h5 info as a dictionary with keys for
'cross section', 'energy', 'element' and other info on the nuclius

```python
import openmc_data_to_json as odj

reaction = odj.cross_section_from_h5_to_dict(
    input='Be9.h5',
    reaction='(n,2n)'
)
```

A h5 file can be checked for reactions to see if particular reactions exist

```python
import openmc_data_to_json as odj

reaction = odj.reactions_in_h5(
    input='Fe56.h5',
    reaction='(n,g)'
)
```


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
