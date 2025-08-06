import json
import numpy as np
import openmc
from typing import Optional


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


def extract_cross_section_data(h5_filename, json_filename: Optional[str] = None):
    # --- Add sum rules for hierarchical MTs ---
    SUM_RULES = {
        1: [2, 3],
        3: [4, 5, 11, 16, 17, 22, 23, 24, 25, 27, 28, 29, 30, 32, 33, 34, 35,
            36, 37, 41, 42, 44, 45, 152, 153, 154, 156, 157, 158, 159, 160,
            161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172,
            173, 174, 175, 176, 177, 178, 179, 180, 181, 183, 184, 185,
            186, 187, 188, 189, 190, 194, 195, 196, 198, 199, 200],
        4: list(range(50, 92)),
        16: list(range(875, 892)),
        18: [19, 20, 21, 38],
        27: [18, 101],
        101: [102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114,
              115, 116, 117, 155, 182, 191, 192, 193, 197],
        103: list(range(600, 650)),
        104: list(range(650, 700)),
        105: list(range(700, 750)),
        106: list(range(750, 800)),
        107: list(range(800, 850)),
    }

    result = {}

    isotope_object = openmc.data.IncidentNeutron.from_hdf5(h5_filename)
    result['atomic_number'] = isotope_object.atomic_number
    result['atomic_symbol'] = isotope_object.atomic_symbol
    result['atomic_weight_ratio'] = isotope_object.atomic_weight_ratio
    result['mass_number'] = isotope_object.mass_number
    result['metastable'] = isotope_object.metastable
    result['nuclide'] = isotope_object.name
    result['temperatures'] = [str(temp).replace('K', '') for temp in isotope_object.temperatures]

    result['reactions'] = {}

    # Collect all unique temperatures first
    all_temperatures = set()
    for reaction in isotope_object.reactions.values():
        all_temperatures.update(str(temp).replace('K', '') for temp in reaction.xs.keys())

    # Initialize the nested structure once
    for temperature in all_temperatures:
        result['reactions'][temperature.replace('K', '')] = {}

    result['energy'] = {}
    for temperature, energy in isotope_object.energy.items():
        result['energy'][temperature.replace('K', '')] = energy

    for reaction_mt, reaction in isotope_object.reactions.items():
        temperatures_and_tabulars = reaction.xs

        for temperature, tabular in temperatures_and_tabulars.items():
            reaction_at_temperature_dict = {}

            reaction_at_temperature_dict['interpolation'] = tabular.interpolation
            reaction_at_temperature_dict['threshold_idx'] = tabular._threshold_idx
            reaction_at_temperature_dict['xs'] = tabular.y

            # Always use string keys for MTs
            result['reactions'][temperature.replace('K', '')][str(reaction_mt)] = reaction_at_temperature_dict

            # print(f"Reaction MT: {reaction_mt}, Temperature: {temperature}, Interpolation: {tabular.interpolation}, Threshold Index: {tabular._threshold_idx}, len XS: {len(tabular.x)}")


    # After all explicit reactions are loaded, iteratively generate all possible hierarchical MTs
    for temperature in result['reactions']:
        reactions_at_temp = result['reactions'][temperature]
        available_mts = set(str(mt) for mt in reactions_at_temp.keys())
        constructed = set()
        print(f"\n--- Debug for temperature {temperature} ---")
        print(f"Available MTs: {sorted(available_mts)}")
        # Keep trying to build new MTs until no more can be built
        while True:
            added = False
            # Work through sum rules in reverse order
            for mt, children in reversed(list(SUM_RULES.items())):
                mt_str = str(mt)
                if mt_str in reactions_at_temp:
                    continue  # Already present
                present_children = [str(child) for child in children if str(child) in available_mts]
                missing_children = [str(child) for child in children if str(child) not in available_mts]
                if not present_children:
                    print(f"Cannot construct MT {mt_str} at temperature {temperature}: no children available")
                    continue
                # Get the energy grid for this temperature
                energy_grid = result['energy'][temperature]
                grid_len = len(energy_grid)
                # Align all child xs arrays to the energy grid using threshold_idx
                aligned_arrays = []
                min_threshold_idx = grid_len  # Start with max possible
                for child in present_children:
                    child_xs = np.array(reactions_at_temp[child]['xs'])
                    child_threshold_idx = reactions_at_temp[child]['threshold_idx']
                    min_threshold_idx = min(min_threshold_idx, child_threshold_idx)
                    arr = np.zeros(grid_len)
                    arr[child_threshold_idx:child_threshold_idx+len(child_xs)] = child_xs
                    aligned_arrays.append(arr)
                # Sum the aligned arrays
                summed_xs_full = np.sum(aligned_arrays, axis=0)
                # The hierarchical MT's threshold_idx is min of children
                summed_xs = summed_xs_full[min_threshold_idx:]
                interp = reactions_at_temp[present_children[0]]['interpolation']
                reactions_at_temp[mt_str] = {
                    'interpolation': interp,
                    'threshold_idx': min_threshold_idx,
                    'xs': summed_xs.tolist(),
                }
                print(f"Constructed new MT {mt_str} at temperature {temperature} using children {present_children}. Missing: {missing_children}")
                available_mts.add(mt_str)
                constructed.add(mt_str)
                added = True
            if not added:
                break


    if json_filename is None:
        json_filename = f'{isotope_object.name}.json'
    # Sort MTs in each temperature's reactions by integer value before writing
    for temperature in result['reactions']:
        reactions = result['reactions'][temperature]
        # Sort keys numerically
        sorted_reactions = dict(sorted(reactions.items(), key=lambda x: int(x[0])))
        result['reactions'][temperature] = sorted_reactions

    with open(json_filename, 'w') as f:
        json.dump(result, f, cls=CompactJSONEncoder, indent=2)

    return result
