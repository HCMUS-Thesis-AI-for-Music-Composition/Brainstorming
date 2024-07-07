from const_lib import musecoco_const as mcc
import random

# INITIALIZE
abbreviations = {
    "b": "bar",
    "o": "position",
    "s": "time_signature",
    "t": "tempo",
    "i": "instrument",
    "p": "pitch",
    "d": "duration",
    "v": "velocity",
    "n": "pitch_name",
    "c": "pitch_octave",
    "f": "family",
    "e": "special"
}

reversed_abbrs = {v: k for k, v in abbreviations.items()}

inappropriate_head_keys = ['d', 'v']
inappropriate_tail_keys = ['p', 'd']

def all_available_structure(next_acceptable_keys):
    '''
        List all possible paths in the graph (if a path meets the start of itself, stop searching on that path)
        Return a list of all possible paths

        next_acceptable_keys: a adjacency list of all possible next keys. Example:
            {
                's': ['b', 'o'],
                'o': ['t'],
                't': ['i'],
                'i': ['p'],
                'p': ['d'],
                'd': ['v'],
                'v': ['i', 'b', 'p', 'o'],
                'b': ['s']
            }

        Return: a list of all possible paths. Example:
            [
                ['s', 'b'],
                ['s', 'o', 't', 'i', 'p', 'd', 'v'],
                ...
            ]
    '''
    paths = []

    def dfs(node: str, path: list):
        if node in path:
            paths.append(path)
            return
        else:
            pass

        path.append(node)
        
        for next_node in next_acceptable_keys[node]:
            dfs(next_node, path.copy())

    for k in next_acceptable_keys.keys():
        dfs(k, [])

    return paths

structures = all_available_structure(mcc.next_acceptable_keys)

def remove_duplicate_structures(
    structures, 
    should_sort_by_length=True, 
    descending_length=True
):
    '''
        Remove duplicate structures in the list of structures
        Return a list of unique structures

        structures: a list of structures. Example:
            [
                ['s', 'b'],
                ['s', 'b'],
                ['s', 'o', 't', 'i', 'p', 'd', 'v'],
                ...
            ]
        
        should_sort_by_length: a boolean value to sort the list of unique structures by length or not. Default is True.

        descending_length: a boolean value to sort the list of unique structures by descending length or not. Default is True.

        Return: a list of unique structures. Example:
            [
                ['s', 'b'],
                ['s', 'o', 't', 'i', 'p', 'd', 'v'],
                ...
            ]
    '''
    # Unique structure
    unique_structures = set([tuple(structure) for structure in structures])
    unique_structures = [list(structure) for structure in unique_structures]

    if should_sort_by_length:
        unique_structures = sorted(
            unique_structures, 
            key=lambda x: len(x), reverse=descending_length
        )
    else:
        pass

    return unique_structures

unique_structures = remove_duplicate_structures(structures)

appropriate_structures = []

# Remove inappropriate structures (inappropriate head/tail keys)
for new_structure in unique_structures:
    if new_structure[0] in inappropriate_head_keys:
        pass
    elif new_structure[-1] in inappropriate_tail_keys:
        pass
    else:
        appropriate_structures.append(new_structure)

golden_head = 's'
golden_tail = 'v'

golden_structures: list[list[str]] = []

for new_structure in appropriate_structures:
    if new_structure[0] == golden_head and new_structure[-1] == golden_tail:
        golden_structures.append(new_structure)

golden_structure = min(golden_structures, key=lambda x: len(x))

# END INITIALIZE


def musecoco_tokens_list_to_token_list_lines_converter(
    musecoco_tokens_list: list[tuple[str, int]],
    line_separators: list[str] = ['position', 'time_signature']
):
    """
        Convert a list of musecoco tokens to a list of lines using line separators (keep the separators in their own). Each line is a list of musecoco tokens.

        musecoco_tokens_list: a list of musecoco tokens. Example: [('i', 40), ('p', 68), ('d', 6), ('v', 20)].

        line_separators: a list of keys to separate lines. Default is ['position', 'time_signature'].

        Return: a list of lines. Each line is a list of musecoco tokens. Example: [[('i', 40), ('p', 68)], [('d', 6), ('v', 20)]].
    """
    lines = []

    line_separators = ['position', 'time_signature']
    line_separators = [reversed_abbrs[key] for key in line_separators]

    current_line = [musecoco_tokens_list[0]]

    for i in range(1, len(musecoco_tokens_list)):
        key, value = musecoco_tokens_list[i]

        if key in line_separators:
            lines.append(current_line)
            current_line = [musecoco_tokens_list[i]]
        else:
            current_line.append(musecoco_tokens_list[i])

    if len(current_line) > 0:
        lines.append(current_line)
    else:
        pass

    return lines

def is_token_list_valid(
    token_list: list[tuple[str, int]],
    next_acceptable_keys: dict[str, list[str]] = mcc.next_acceptable_keys,
):
    """
        Check if the list of tokens is valid or not by checking if the next key of each key in the list is in the adjacency list of its next acceptable keys

        token_list: a list of tokens. Example: [('i', 40), ('p', 68), ('d', 6), ('v', 20)]

        next_acceptable_keys: a adjacency list of all possible next keys. Example: {'s': ['b', 'o'], 'o': ['t'], ...}

        Return: a boolean value to check if the list of tokens is valid or not
    """
    for i in range(len(token_list) - 1):
        try:
            key, value = token_list[i]
            next_key = token_list[i + 1][0]

            if next_key not in next_acceptable_keys[key]:
                return False
        except:
            print(f"Error at index {i}: {token_list[i]}")
            return False
        
    return True

def nearest_valid_line(
    target_line_idx, 
    are_lines_valid: list[bool]
):
    """
        Find the nearest valid line to the target line (previous lines first, then next lines)
        Return the index of the nearest valid line

        target_line_idx: the index of the target line to find the nearest valid line
        are_lines_valid: a list of boolean values to check if the line is valid or not

        Return: the index of the nearest valid line
    """
    nearest_valid_line_idx = -1
    
    for i in range(target_line_idx - 1, -1, -1):
        if are_lines_valid[i]:
            nearest_valid_line_idx = i
            break
        else:
            pass
    if nearest_valid_line_idx == -1:
        for i in range(target_line_idx + 1, len(are_lines_valid)):
            if are_lines_valid[i]:
                nearest_valid_line_idx = i
                break
            else:
                pass
    else:
        pass

    result = nearest_valid_line_idx if nearest_valid_line_idx >= 0 else None

    return result

def copy_line_a_structure_to_line_b(
    musecoco_tokens_list_a: list[tuple[str, int]],
    musecoco_tokens_list_b: list[tuple[str, int]]
):
    """
        Copy the structure (the keys) of line a to line b. Use the value from line b if the target key exists in line b.
    """
    new_line_b = musecoco_tokens_list_a.copy()

    old_line_b_dict = {k: v for k, v in musecoco_tokens_list_b}
    
    for i in range(len(new_line_b)):
        key, value = new_line_b[i]
        if key in old_line_b_dict.keys():
            new_line_b[i] = (key, old_line_b_dict[key])
        else:
            # Keep the original value of line b
            pass

    return new_line_b

def are_all_list_elements_equal_to_value(
    list_to_check: list,
    value
):
    for element in list_to_check:
        if element != value:
            return False
        else:
            pass

    return True

def token_list_to_key_only_str(token_list: list[tuple[str, int]]):
    return "".join([pair[0] for pair in token_list])

def fix_error_for_first_token_line(
    musecoco_token_lines: list[list[tuple[str, int]]],
    new_structure: list[str] = golden_structure,
    inappropriate_head_keys: list[str] = ['d', 'v'],
):
    """
        Fix the error for the first line of the list of musecoco tokens. If the first line is invalid, fill it with a suitable structure.

        musecoco_token_lines: a list of musecoco tokens. Example: 
        
            [
                [('i', 40), ('p', 68)], 
                
                [('d', 6), ('v', 20)]
            ]

        new_structure: a list of keys to fill the first line. Default is the golden structure.

        inappropriate_head_keys: a list of keys that are inappropriate to be the head key of the first line. Default is ['d', 'v'].

        Return: a list of musecoco tokens with the first line is valid.
    """
    is_first_line_valid = is_token_list_valid(musecoco_token_lines[0])

    is_first_key_valid = musecoco_token_lines[0][0][0] not in inappropriate_head_keys
    
    if is_first_line_valid and is_first_key_valid:
        pass
    else:
        new_first_line: list[tuple[str, int]] = []

        values_for_each_key = {
            key: set()
            for key in new_structure
        }

        for line in musecoco_token_lines:
            for key, value in line:
                values_for_each_key[key].add(value)

        for key in new_structure:
            if len(values_for_each_key[key]) > 0:
                pass
            else:
                print(f"Key {key} has no value. Fill with 0.")
                
                # Brainstorming/MIDI/Ideas/vocab_manager_dict.json
                four_four_time_signature = 9
                
                values_for_each_key[key].add(
                    four_four_time_signature
                )

            values_for_each_key[key] = list(values_for_each_key[key])

        for key in new_structure:
            n_values_for_key = len(values_for_each_key[key])
            
            start_idx = 0
            end_idx = n_values_for_key - 1 if n_values_for_key > 1 else 0

            random_value_idx = random.randint(start_idx, end_idx)

            random_value = values_for_each_key[key][random_value_idx]

            new_first_line.append((key, random_value))

        musecoco_token_lines[0] = new_first_line

    return musecoco_token_lines

def nearest_line_fill(
    musecoco_tokens_list: list[tuple[str, int]]
) -> list[tuple[str, int]]:
    """
        Fill the missing lines by the nearest valid line's structure. If the first line is invalid, fill it with a suitable structure.

        musecoco_tokens_list: a list of musecoco tokens. Example: [('i', 40), ('p', 68), ('d', 6), ('v', 20)].

        Return: a token list with all tokens are valid. Example: [('i', 40), ('p', 68), ('d', 6), ('v', 20)].
    """
    musecoco_token_lines = musecoco_tokens_list_to_token_list_lines_converter(
        musecoco_tokens_list
    )

    are_lines_valid = []
    for line in musecoco_token_lines:
        are_lines_valid.append(is_token_list_valid(line))

    if are_all_list_elements_equal_to_value(are_lines_valid, True):
        pass
        # return musecoco_token_lines
    elif are_all_list_elements_equal_to_value(are_lines_valid, False):
        print("All lines are invalid. Cannot apply by_line_nearest_fill.")
        return None
    else:
        # Fix the first line if it is invalid
        musecoco_token_lines = fix_error_for_first_token_line(musecoco_token_lines)

        for i in range(len(are_lines_valid)):
            if not are_lines_valid[i]:
                nearest_valid_line_idx = nearest_valid_line(i, are_lines_valid)
                
                if nearest_valid_line_idx is not None:
                    musecoco_token_lines[i] = copy_line_a_structure_to_line_b(
                        musecoco_token_lines[nearest_valid_line_idx],
                        musecoco_token_lines[i]
                    )

                    # Validate the line's tail key (if it is invalid, choose a suitable structure to fill)
                else:
                    raise ValueError(f"fill_missing_by_line: Cannot find any valid line to fill line {i}")

    result = [pair for line in musecoco_token_lines for pair in line]

    return result

