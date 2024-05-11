import re

from dto.Note import NoteDTO
from converter.note_position import position_to_tick_converter

# {
#     "sd": "1",
#     "octave": 0, = C4
#     "beat": 1,
#     "duration": 2,
#     "isRest": true,
#     "recordingEndBeat": null
# }

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

inversed_based_midi_note_numbers = {
    note: midi_note_number
    for midi_note_number, notes in based_midi_note_numbers.items()
    for note in notes
}

C4_midi_note_number = 60

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

hooktheory_ticks_per_beat = 960

class SongKey:
    def __init__(self, root_note_str: str, scale: str):
        self.root_note_str = root_note_str
        self.scale_name = scale

def hooktheory_beat_to_tick_position(
    beat: float,
    ticks_per_beat: int = hooktheory_ticks_per_beat
) -> int:
    return position_to_tick_converter(
        position=beat - 1,
        tick_per_beat=ticks_per_beat,
        position_resolution=1
    )

def hooktheory_duration_to_tick_duration(
    duration: float,
    ticks_per_beat: int = hooktheory_ticks_per_beat
) -> int:
    return position_to_tick_converter(
        position=duration,
        tick_per_beat=ticks_per_beat,
        position_resolution=1
    )

def calculate_note_end_tick_position(
    hooktheory_start_beat: float,
    hooktheory_duration: float,
    ticks_per_beat: int = hooktheory_ticks_per_beat
) -> int:
    return (
        hooktheory_beat_to_tick_position(
            hooktheory_start_beat,
            ticks_per_beat
        ) + hooktheory_duration_to_tick_duration(
            hooktheory_duration,
            ticks_per_beat
        )
    )

def scale_degree_to_midi_note_number(
    scale_degree_str: str,
    key: SongKey,
    octave: int = 0
):
    # Check if sd is n, bn or #n
    accidental_semitones = 0

    if re.match(r"^\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str)
    elif re.match(r"^b\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str[1:])
        accidental_semitones = -1
    elif re.match(r"^\#\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str[1:])
        accidental_semitones = 1

    root_midi_note_number = inversed_based_midi_note_numbers[key.root_note_str]
    scale_formula = scale_formulas[key.scale_name]
    
    base_midi_note = root_midi_note_number + sum(scale_formula[:(scale_degree - 1)]) + accidental_semitones
    
    return base_midi_note + 12 * octave + C4_midi_note_number


def json_notes_converter(notes: list) -> list[NoteDTO]:
    converted_notes = []
    for note in notes:
        converted_notes.append(
            NoteDTO(
                start=note["start"],
                end=note["end"],
                pitch=note["pitch"],
                velocity=note["velocity"]
            )
        )
    return converted_notes
