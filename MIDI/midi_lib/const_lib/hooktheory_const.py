import const.midi as mc

hooktheory_ticks_per_beat = 960
hooktheory_default_velocity = 80

hooktheory_default_instr_program = 0
hooktheory_default_instr_name = mc.midi_program_to_instrument_name_mapper[
    hooktheory_default_instr_program
]

hooktheory_default_melody_instrument_programs = [
    0, # Acoustic Grand Piano
    22, # Harmonica
    24,	# Guitar Acoustic Guitar (nylon)
    25,	# Guitar Acoustic Guitar (steel)
    27, # Electric Guitar (clean)
    29, # Overdriven Guitar
    30, # Distortion Guitar
    40, # Violin
    52, # Choir Aahs
    53 # Voice Oohs
]

hooktheory_default_chord_instrument_programs = [
    0, # Acoustic Grand Piano
    3, # Honky-tonk Piano
    4, # Rhodes Piano
    2, # Electric Grand Piano
    8, # Celesta
    16, # Hammond Organ
    21, # Accordion
    41, # Viola
    61, # Brass Section
    90 # Pad 3 (polysynth)
]

# melodies velocity - chords velocity
velocity_delta = 10

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