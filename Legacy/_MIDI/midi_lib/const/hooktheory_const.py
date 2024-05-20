import const.midi as mc

hooktheory_ticks_per_beat = 960
hooktheory_default_velocity = 80

hooktheory_default_instr_program = 0
hooktheory_default_instr_name = mc.midi_program_to_instrument_name_mapper[
    hooktheory_default_instr_program
]

chord_default_octave = -1

n_octave_lower_for_bass_notes = 2

beat_unit_to_time_signature_denominator_mapper = {
    1: 4,
    3: 8
}

class HookTheoryKeySignatureDTO:
    def __init__(self, root_note_str: str, scale: str):
        """
            root_note_str: str. Example: "C", "D#", "Bb", etc.
            scale: str. Example: "major", "minor", "dorian", "lydian", "phrygian", "locrian", "harmonicMinor", "mixolydian", etc.
        """
        self.root_note_str = root_note_str
        self.scale_name = scale

