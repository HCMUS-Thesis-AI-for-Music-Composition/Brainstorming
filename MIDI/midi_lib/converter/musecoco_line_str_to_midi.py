from datetime import datetime
import os

from converter.midi_dto_to_midi_file_object import midi_dto_to_midi_file_object_converter
from converter.musecoco_line_to_midi_dto import musecoco_line_to_midi_dto_converter
from converter.musecoco_line_str_to_token_list import musecoco_line_str_to_token_list_converter
from musecoco_utils import remove_structure_errors

from fill_missing import nearest_line_fill as fill_nearest

from midi_file_utils import write_midi_file

# Use set_default_values to set the 3 values below (if needed)
output_dir = "/Users/4rr311/Documents/VectorA/KHTN/Nam4/HKII/Thesis/Brainstorming/MIDI/Ideas/data/output"

log_dir = "/Users/4rr311/Documents/VectorA/KHTN/Nam4/HKII/Thesis/Brainstorming/MIDI/Ideas/hooktheory/output/logs/model_result_log"

mid_file_name_prefix = "result"

# 2 values below will be set later in the default_setup function
log_index_folder_path = ""

default_midi_file_name = "" 

def set_default_values(
    output_path=output_dir,
    log_path=log_dir,
    midi_file_name_prefix=mid_file_name_prefix
):
    """
        Set the default values for the module

        Parameters:
            output_path (str): The path to the output folder
            log_path (str): The path to the log folder
            midi_file_name_prefix (str): The prefix for the midi file name
    """
    global output_dir
    global log_dir
    global mid_file_name_prefix

    output_dir = output_path
    log_dir = log_path
    mid_file_name_prefix = midi_file_name_prefix

def get_current_time():
    now = datetime.now()

    dd = int(now.strftime("%d"))
    mm = int(now.strftime("%m"))
    yyyy = int(now.strftime("%Y"))
    hh = int(now.strftime("%H"))


    am_pm = None
    if hh > 12:
        hh = hh - 12
        am_pm = "pm"
    else:
        am_pm = "am"

    # Make dd, mm, hh 2 digits
    dd = f"{'0' * (2 - len(str(dd)))}{dd}"
    mm = f"{'0' * (2 - len(str(mm)))}{mm}"
    hh = f"{'0' * (2 - len(str(hh)))}{hh}"

    return {
        "dd": dd,
        "mm": mm,
        "yyyy": yyyy,
        "hh": hh,
        "am_pm": am_pm
    }

# SETUP THE OUTPUT AND LOG FOLDERS
def default_setup():
    global log_index_folder_path
    global default_midi_file_name

    current_time = get_current_time()

    yyyy_mm_dd = "_".join([
        str(current_time["yyyy"]), 
        str(current_time["mm"]), 
        str(current_time["dd"])
    ])

    hh_am_pm = "_".join([
        str(current_time["hh"]),
        str(current_time["am_pm"])
    ])

    log_date_folder_path = f"{log_dir}/{yyyy_mm_dd}"
    log_time_folder_path = f"{log_date_folder_path}/{hh_am_pm}"

    # Create the folders if it does not exist (recursive)
    if not os.path.exists(log_date_folder_path):
        # os.mkdir(log_date_folder_path)
        os.makedirs(log_date_folder_path)

    if not os.path.exists(log_time_folder_path):
        # os.mkdir(log_time_folder_path)
        os.makedirs(log_time_folder_path)

    # Count the number of folders in the log_date_folder_path (excluding the .DS_Store file)
    log_date_folders = [f for f in os.listdir(log_date_folder_path) if not f.startswith('.')]

    n_log_time_folders = 0
    # Count log time folders in each log date folder
    for log_date_folder in log_date_folders:
        log_time_folder = f"{log_date_folder_path}/{log_date_folder}"
        
        # Count the number of folders in the log_time_folder (excluding the .DS_Store file)
        log_time_folders = [f for f in os.listdir(log_time_folder) if not f.startswith('.')]
        n_log_time_folders += len(log_time_folders)

    midi_index = n_log_time_folders

    log_index_folder_path = f"{log_time_folder_path}/{midi_index}"

    if not os.path.exists(log_index_folder_path):
        os.mkdir(log_index_folder_path)

    default_midi_file_name = f"{mid_file_name_prefix}_{yyyy_mm_dd}_{hh_am_pm}_{midi_index}.mid"

# LOG FUNCTIONS
def midi_number_to_note_name(midi_number):
    '''
        Convert a midi number to a note name
    '''
    notes = [
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
    ]

    note = notes[midi_number % 12]
    octave = midi_number // 12 - 1

    return f"{note}{octave}"

def print_key_value_line(key_value_line):
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

    printed_lines = ""

    if key_value_line == None or key_value_line == []:
        printed_lines += "None or Empty\n"
        printed_lines += str(key_value_line)
        return printed_lines
    
    n_space_for_digits = 5

    n_letter_per_print_time_for_abbrs = {
        x : len(abbreviations[x]) + n_space_for_digits
        for x in abbreviations
    }

    for pair in key_value_line:
        # print(pair)
        # print(key_value_line)
        key, value = pair

        converted_value = None

        if abbreviations[key] == 'pitch':
            converted_value = int(value)
            converted_value = midi_number_to_note_name(int(value))
        else:
            converted_value = ''

        abbr_meaning = abbreviations[key]

        pair_str = f"{abbr_meaning}: {value} {converted_value}"
        end_spaces = ' ' * (n_letter_per_print_time_for_abbrs[key] - len(abbr_meaning) - len(str(value)))

        if abbr_meaning in ['position', 'time_signature']:
            printed_lines += "\n"

        printed_lines += pair_str + end_spaces

    return printed_lines

# CONVERTER
def musecoco_line_str_to_midi_converter(
    musecoco_line_str: str,
    output_midi_file_name: str = None,
    should_fill_missing: bool = True
) -> tuple[str, str, str]:
    """
        Convert a musecoco line string to a midi file

        Parameters:
            musecoco_line_str (str): The musecoco line string

        Returns:
            (
                midi_file_path (str): The path to the converted midi file,
                original_structure_log_file_path (str): The path to the original structure log file,
                log_file_path (str): The path to the log file
            )
    """
    default_setup()

    if output_midi_file_name == None:
        output_midi_file_name = default_midi_file_name
    else:
        pass

    model_result_tokens_list = musecoco_line_str_to_token_list_converter(musecoco_line_str)

    # Fill missing data
    if should_fill_missing:
        model_result_tokens_list = fill_nearest.nearest_line_fill(model_result_tokens_list)
    else:
        pass

    # Log the original structure
    printed_lines = print_key_value_line(model_result_tokens_list)

    original_structure_log_file_path = f"{log_index_folder_path}/original_structure.txt"

    with open(original_structure_log_file_path, "w") as f:
        f.write(printed_lines)

    # Convert token list to MIDI
    output_midi_file_path = f"{output_dir}/{output_midi_file_name}"

    model_result_tokens_list, printed_lines = remove_structure_errors(model_result_tokens_list)

    midi_dto = musecoco_line_to_midi_dto_converter(
        model_result_tokens_list,
        tick_per_beat=480
    )

    midi_obj = midi_dto_to_midi_file_object_converter(midi_dto)

    write_midi_file(midi_obj, output_midi_file_path)

    printed_lines = f"{output_midi_file_path}\n{printed_lines}"

    wrong_structure_log_file_path = f"{log_index_folder_path}/wrong_structure_log.txt"

    with open(wrong_structure_log_file_path, "w") as f:
        f.write(printed_lines)

    return (
        output_midi_file_path,
        original_structure_log_file_path,
        wrong_structure_log_file_path
    )
