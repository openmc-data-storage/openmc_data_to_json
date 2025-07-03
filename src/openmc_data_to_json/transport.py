import json
import numpy as np
import openmc

class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts arrays of primitives on a single line."""

    def __init__(self, *args, **kwargs):
        # Default to 2-space indentation if not specified
        if kwargs.get("indent") is None:
            kwargs["indent"] = 2
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def default(self, o):
        """Handle NumPy types"""
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        return json.JSONEncoder.default(self, o)

    def encode(self, o):
        """Encode JSON objects with special handling for arrays of primitives."""
        if isinstance(o, (list, tuple)):
            # Put arrays of primitives on a single line
            if all(isinstance(x, (int, float, bool, str, type(None))) for x in o):
                return "[" + ", ".join(json.dumps(el) for el in o) + "]"
            # For other containers, use standard formatting
            return self._encode_container(o, "[", "]")
        if isinstance(o, dict):
            if not o:
                return "{}"
            # Ensure keys are strings
            o = {str(k) if k is not None else "null": v for k, v in o.items()}
            if self.sort_keys:
                o = dict(sorted(o.items(), key=lambda x: x[0]))
            # Format dictionary
            return self._encode_container(o, "{", "}")
        # For primitive types, use standard JSON encoding
        return json.dumps(
            o,
            skipkeys=self.skipkeys,
            ensure_ascii=self.ensure_ascii,
            check_circular=self.check_circular,
            allow_nan=self.allow_nan,
            sort_keys=self.sort_keys,
            separators=(self.item_separator, self.key_separator),
            default=self.default,
        )

    def _encode_container(self, container, open_char, close_char):
        """Encode a container with proper indentation."""
        is_dict = isinstance(container, dict)
        
        # Handle very small containers on single line (dicts with 1 item or less)
        if is_dict and len(container) <= 1:
            if not container:
                return "{}"
            key, value = next(iter(container.items()))
            return f"{{ {self.encode(key)}: {self.encode(value)} }}"
        
        # Format container across multiple lines
        self.indentation_level += 1
        if is_dict:
            items = [f"{self.indent_str}{self.encode(k)}: {self.encode(v)}" for k, v in container.items()]
        else:
            items = [f"{self.indent_str}{self.encode(el)}" for el in container]
        self.indentation_level -= 1
        
        return f"{open_char}\n" + ",\n".join(items) + f"\n{self.indent_str}{close_char}"

    def iterencode(self, data, **kwargs):
        """Required to also work with `json.dump`."""
        return self.encode(data)

    @property
    def indent_str(self) -> str:
        """Get the indentation string for the current level."""
        if isinstance(self.indent, int):
            return " " * (self.indentation_level * self.indent)
        elif isinstance(self.indent, str):
            return self.indentation_level * self.indent
        else:
            return ""


def extract_cross_section_data(h5_filename, json_filename):
    result = {}

    isotope_object = openmc.data.IncidentNeutron.from_hdf5(h5_filename)
    result['atomic_number'] = isotope_object.atomic_number
    result['atomic_symbol'] = isotope_object.atomic_symbol
    result['atomic_weight_ratio'] = isotope_object.atomic_weight_ratio
    result['mass_number'] = isotope_object.mass_number
    result['metastable'] = isotope_object.metastable
    result['nuclide'] = isotope_object.name
    result['temperatures'] = isotope_object.temperatures

    result['reactions'] = {}

    # Collect all unique temperatures first
    all_temperatures = set()
    for reaction in isotope_object.reactions.values():
        all_temperatures.update(reaction.xs.keys())
    
    # Initialize the nested structure once
    for temperature in all_temperatures:
        result['reactions'][temperature] = {}

    result['energy'] = {}
    for temperature, energy in isotope_object.energy.items():
        result['energy'][temperature] = energy

    for reaction_mt, reaction in isotope_object.reactions.items():
        temperatures_and_tabulars=reaction.xs

        for temperature, tabular in temperatures_and_tabulars.items():       
            reaction_at_temperature_dict = {}

            reaction_at_temperature_dict['interpolation'] = tabular.interpolation
            reaction_at_temperature_dict['threshold_idx'] = tabular._threshold_idx
            reaction_at_temperature_dict['xs'] = tabular.x

            result['reactions'][temperature][reaction_mt] = reaction_at_temperature_dict

            # print(f"Reaction MT: {reaction_mt}, Temperature: {temperature}, Interpolation: {tabular.interpolation}, Threshold Index: {tabular._threshold_idx}, len XS: {len(tabular.x)}")

    with open(json_filename, 'w') as f:
        json.dump(result, f, cls=CompactJSONEncoder, indent=2)

    return result
