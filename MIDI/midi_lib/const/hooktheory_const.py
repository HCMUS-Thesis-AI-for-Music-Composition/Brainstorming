import const.midi as mc

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
hooktheory_default_velocity = 80

hooktheory_default_instr_program = 0
hooktheory_default_instr_name = mc.midi_program_to_instrument_name_mapper[
    hooktheory_default_instr_program
]

class HookTheoryKeySignatureDTO:
    def __init__(self, root_note_str: str, scale: str):
        self.root_note_str = root_note_str
        self.scale_name = scale
