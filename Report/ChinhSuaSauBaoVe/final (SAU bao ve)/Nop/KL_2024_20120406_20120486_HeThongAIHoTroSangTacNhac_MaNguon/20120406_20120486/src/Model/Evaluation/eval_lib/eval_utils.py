import copy
import eval_lib.eval_config as ec

import sys
sys.path.append(ec.midi_lib_dir)

from dto.Midi import MidiDTO
from dto.KeySignatureChange import KeySignatureChangeDTO
from converter.midi_file_object_to_midi_dto import midi_file_object_to_midi_dto_converter
import midi_file_utils as mfu

C4_midi_note_number = 60
A0_midi_note_number = 21
C8_midi_note_number = 108

min_midi_note_number = 0
max_midi_note_number = 127
notes_per_octave = 12

min_midi_note_number_on_piano = A0_midi_note_number
max_midi_note_number_on_piano = C8_midi_note_number

based_midi_note_numbers = {
    0: ["C"],
    1: ["C#", "Db"],
    2: ["D"],
    3: ["D#", "Eb"],
    4: ["E"],
    5: ["F"],
    6: ["F#", "Gb"],
    7: ["G"],
    8: ["G#", "Ab"],
    9: ["A"],
    10: ["A#", "Bb"],
    11: ["B"]
}

class ScaleName:
    MAJOR = "major"
    MINOR = "minor"
    HARMONIC_MINOR = "harmonic_minor"
    DORIAN = "dorian"

scale_formulas = {
    ScaleName.MAJOR: [2, 2, 1, 2, 2, 2, 1],
    ScaleName.MINOR: [2, 1, 2, 2, 1, 2, 2],
    ScaleName.HARMONIC_MINOR: [2, 1, 2, 2, 1, 3, 1],
    ScaleName.DORIAN: [2, 1, 2, 2, 2, 1, 2]
}

inversed_scale_formulas = {
    str(v) : k
    for k, v in scale_formulas.items()
}

common_notes_per_scale = 7

key_signature_prototypes = {
    "C major": [
        (sum(scale_formulas["major"][0:i]) + C4_midi_note_number) % notes_per_octave
        for i in range(len(scale_formulas["major"]))
    ],
    "A minor": [
        (sum(scale_formulas["minor"][0:i]) + A0_midi_note_number) % notes_per_octave
        for i in range(len(scale_formulas["minor"]))
    ],
    "A harmonic minor": [
        (sum(scale_formulas["harmonic_minor"][0:i]) + A0_midi_note_number) % notes_per_octave
        for i in range(len(scale_formulas["harmonic_minor"]))
    ]
}

def is_accidental_midi_note_number(midi_note_number: int):
    return not (
        1 == len(based_midi_note_numbers[
            midi_note_number % notes_per_octave
        ])
    )

def key_signature_from_midi_note_numbers(midi_note_numbers: list, root_note_number: int = None):
    """
    Get the key signature of a song from the midi note numbers (single key detection, no key modulation processing).
    :param midi_note_numbers: the midi note numbers
    :param root_note_number: the root note number
    :return: the key signature. Example: (0, "major") for C major, (9, "minor") for A minor, etc.
    """

    midi_note_numbers = list(set(midi_note_numbers))

    print("MIDI NOTE NUMBERS: ", midi_note_numbers)
    
    
    midi_note_numbers = sorted([
        note_number % notes_per_octave
        for note_number in midi_note_numbers
    ])

    print("SORTED MIDI NOTE NUMBERS: ", midi_note_numbers)

    root_note_idx = None

    root_note_number = (root_note_number % notes_per_octave) if root_note_number != None else None

    if root_note_number == None:
        root_note_idx = 0
        root_note_number = midi_note_numbers[root_note_idx]
    elif root_note_number not in midi_note_numbers:
        raise ValueError("key_signature_from_midi_note_numbers: The root note number is not in the midi note numbers.")
    else:
        root_note_idx = midi_note_numbers.index(root_note_number)

    midi_note_numbers = midi_note_numbers[root_note_idx:] + midi_note_numbers[:root_note_idx]
    
    root_note_idx = 0

    n_notes = len(midi_note_numbers)

    print("MIDI NOTE NUMBERS BEFORE INTERVALS CAL: ", midi_note_numbers)

    intervals = [
        (
            midi_note_numbers[(i + 1 + n_notes) % n_notes] - midi_note_numbers[i] + notes_per_octave
        ) % notes_per_octave
        for i in range(len(midi_note_numbers))
    ]

    print("Intervals: ", intervals)

    key_signature = None

    root_note_idx = root_note_idx - 1
    for rotating_idx in range(n_notes):
        root_note_idx = (root_note_idx + 1) % n_notes
        root_note_number = midi_note_numbers[root_note_idx]

        key_signature = inversed_scale_formulas.get(
            str(intervals[root_note_idx:] + intervals[:root_note_idx]), 
            None
        )
        
        if key_signature != None:
            break
        else:
            pass
    
    return (root_note_number, key_signature)

def sort_notes_by_start_time(notes: list):
    return sorted(notes, key = lambda note: note.start)

def midi_key_signature_detector(midi_dto: MidiDTO):
    """
    Detect the key signature of a midi file.
    :param midi_file_path: the path of the midi file
    :return: the key signature
    """
    key_changes: list[KeySignatureChangeDTO] = []

    # dict: {key_start_time (int) : notes (set)}
    notes_in_midi: dict = {}

    current_key_start_time: int = None

    current_notes_in_midi = set()

    # Sort notes by start time
    for instr_idx in range(len(midi_dto.instruments)):
        midi_dto.instruments[instr_idx].notes = sort_notes_by_start_time(
            midi_dto.instruments[instr_idx].notes
        )

    print("SORTED")

    current_max_note_end_time = 0

    next_instr_note_indices = {
        instr_idx : 0 
        for instr_idx in range(len(midi_dto.instruments))
    }

    is_n_notes_greater_than_common_notes_per_scale = False

    instrs_note_quantity = {
        instr_idx : len(midi_dto.instruments[instr_idx].notes)
        for instr_idx in range(len(midi_dto.instruments))
    }

    is_all_instrs_notes_read = False
    print("m_instruments: ", len(midi_dto.instruments))
    while not is_n_notes_greater_than_common_notes_per_scale:
        for instr_idx, note_idx in next_instr_note_indices.items():
            # print("instr_idx: ", instr_idx, " note_idx: ", note_idx)
            if note_idx < len(midi_dto.instruments[instr_idx].notes):
                note = midi_dto.instruments[instr_idx].notes[note_idx]
                
                if note.start >= note.end:
                    print("note.start >= note.end")
                    
                if current_key_start_time == None:
                    current_key_start_time = note.start
                else:
                    current_key_start_time = min(
                        current_key_start_time, 
                        note.start
                    )

                current_max_note_end_time = max(
                    current_max_note_end_time, 
                    note.end
                )
                print("break")
                break
            else:          
                is_all_instrs_notes_read = True

                for _instr_idx, _note_idx in next_instr_note_indices.items():
                    if _note_idx < instrs_note_quantity[_instr_idx]:
                        is_all_instrs_notes_read = False
                        break
                    else:
                        pass

                if is_all_instrs_notes_read:
                    print("is_all_instrs_notes_read running...")
                    break
                else:
                    pass

        if is_all_instrs_notes_read:
            print("is_all_instrs_notes_read running...")
            break
        else:
            for instr_idx, note_idx in next_instr_note_indices.items():
                if is_n_notes_greater_than_common_notes_per_scale:
                    print("if is_n_notes_greater_than_common_notes_per_scale running...")
                    is_n_notes_greater_than_common_notes_per_scale = False

                    notes_in_midi[
                        current_key_start_time
                    ] = current_notes_in_midi
                    
                    print("NOTES IN MIDI: ", current_notes_in_midi)
                    
                    current_notes_in_midi = set()

                    break
                else:
                    for i in range(note_idx, len(midi_dto.instruments[instr_idx].notes)):
                        note = midi_dto.instruments[instr_idx].notes[i]

                        if note.start >= current_max_note_end_time:
                            # print("if note.start >= current_max_note_end_time running...")
                            print("     note.start: ", note.start, " current_max_note_end_time: ", current_max_note_end_time)
                            break
                        else:
                            if len(notes_in_midi) == common_notes_per_scale:
                                is_n_notes_greater_than_common_notes_per_scale = True
                                break
                            else:
                                current_notes_in_midi.add(note.pitch % notes_per_octave)

                                next_instr_note_indices[instr_idx] = i + 1

    print("NOTES IN MIDI: ", notes_in_midi)
    for key_start_time, notes in notes_in_midi.items():
        print("KEY START TIME: ", key_start_time, " NOTES: ", notes)
        print("len(notes): ", len(notes))
        key_signature = key_signature_from_midi_note_numbers(notes)
        key_changes.append(
            KeySignatureChangeDTO(
                time = key_start_time,
                key_name = key_signature
            )
        )

    return key_changes