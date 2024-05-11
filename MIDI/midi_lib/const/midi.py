default_ticks_per_beat = 480
default_max_tick = 30721
default_tempo = 120
default_position_resolution = 12
default_velocity = 80

class ScaleName:
    MAJOR = "major"
    MINOR = "minor"
    HARMONIC_MINOR = "harmonicMinor"
    DORIAN = "dorian"

class Accidental:
    FLAT = -1
    SHARP = 1
    NATURAL = 0

default_max_chord_voice_degree = 15

scale_formulas = {
    ScaleName.MAJOR: [2, 2, 1, 2, 2, 2, 1],
    ScaleName.MINOR: [2, 1, 2, 2, 1, 2, 2],
    ScaleName.HARMONIC_MINOR: [2, 1, 2, 2, 1, 3, 1],
    ScaleName.DORIAN: [2, 1, 2, 2, 2, 1, 2]
}

C4_midi_note_number = 60

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

midi_program_to_instrument_name_mapper = {
    1 : "Acoustic Grand Piano",
    2 : "Bright Acoustic Piano",
    3 : "Electric Grand Piano",
    4 : "Honky-Tonk",
    5 : "Electric Piano 1",
    6 : "Electric Piano 2",
    7 : "Harpsichord",
    8 : "Clav",
    9 : "Celesta",
    10 : "Glockenspiel",
    11 : "Music Box",
    12 : "Vibraphone",
    13 : "Marimba",
    14 : "Xylophone",
    15 : "Tubular Bells",
    16 : "Dulcimer",
    17 : "Drawbar Organ",
    18 : "Percussive Organ",
    19 : "Rock Organ",
    20 : "Church Organ",
    21 : "Reed Organ",
    22 : "Accoridan",
    23 : "Harmonica",
    24 : "Tango Accordian",
    25 : "Acoustic Guitar(nylon)",
    26 : "Acoustic Guitar(steel)",
    27 : "Electric Guitar(jazz)",
    28 : "Electric Guitar(clean)",
    29 : "Electric Guitar(muted)",
    30 : "Overdriven Guitar",
    31 : "Distortion Guitar",
    32 : "Guitar Harmonics",
    33 : "Acoustic Bass",
    34 : "Electric Bass(finger)",
    35 : "Electric Bass(pick)",
    36 : "Fretless Bass",
    37 : "Slap Bass 1",
    38 : "Slap Bass 2",
    39 : "Synth Bass 1",
    40 : "Synth Bass 2",
    41 : "Violin",
    42 : "Viola",
    43 : "Cello",
    44 : "Contrabass",
    45 : "Tremolo Strings",
    46 : "Pizzicato Strings",
    47 : "Orchestral Strings",
    48 : "Timpani",
    49 : "String Ensemble 1",
    50 : "String Ensemble 2",
    51 : "SynthStrings 1",
    52 : "SynthStrings 2",
    53 : "Choir Aahs",
    54 : "Voice Oohs",
    55 : "Synth Voice",
    56 : "Orchestra Hit",
    57 : "Trumpet",
    58 : "Trombone",
    59 : "Tuba",
    60 : "Muted Trumpet",
    61 : "French Horn",
    62 : "Brass Section",
    63 : "SynthBrass 1",
    64 : "SynthBrass 2",
    65 : "Soprano Sax",
    66 : "Alto Sax",
    67 : "Tenor Sax",
    68 : "Baritone Sax",
    69 : "Oboe",
    70 : "English Horn",
    71 : "Bassoon",
    72 : "Clarinet",
    73 : "Piccolo",
    74 : "Flute",
    75 : "Recorder",
    76 : "Pan Flute",
    77 : "Blown Bottle",
    78 : "Shakuhachi",
    79 : "Whistle",
    80 : "Ocarina",
    81 : "Lead 1 (square)",
    82 : "Lead 2 (sawtooth)",
    83 : "Lead 3 (calliope)",
    84 : "Lead 4 (chiff)",
    85 : "Lead 5 (charang)",
    86 : "Lead 6 (voice)",
    87 : "Lead 7 (fifths)",
    88 : "Lead 8 (bass+lead)",
    89 : "Pad 1 (new age)",
    90 : "Pad 2 (warm)",
    91 : "Pad 3 (polysynth)",
    92 : "Pad 4 (choir)",
    93 : "Pad 5 (bowed)",
    94 : "Pad 6 (metallic)",
    95 : "Pad 7 (halo)",
    96 : "Pad 8 (sweep)",
    97 : "FX 1 (rain)",
    98 : "FX 2 (soundtrack)",
    99 : "FX 3 (crystal)",
    100 : "FX 4 (atmosphere)",
    101 : "FX 5 (brightness)",
    102 : "FX 6 (goblins)",
    103 : "FX 7 (echoes)",
    104 : "FX 8 (sci-fi)",
    105 : "Sitar",
    106 : "Banjo",
    107 : "Shamisen",
    108 : "Koto",
    109 : "Kalimba",
    110 : "Bagpipe",
    111 : "Fiddle",
    112 : "Shanai",
    113 : "Tinkle Bell",
    114 : "Agogo",
    115 : "Steel Drums",
    116 : "Woodblock",
    117 : "Taiko Drum",
    118 : "Melodic Tom",
    119 : "Synth Drum",
    120 : "Reverse Cymbal",
    121 : "Guitar Fret Noise",
    122 : "Breath Noise",
    123 : "Seashore",
    124 : "Bird Tweet",
    125 : "Telephone Ring",
    126 : "Helicopter",
    127 : "Applause",
    128 : "Gunshot"
}

midi_program_to_instrument_name_mapper = {
    key - 1 : value 
    for key, value in midi_program_to_instrument_name_mapper.items()
}

default_drums_instrument = list(filter(
    lambda x: "Synth Drum".lower() in x[1].lower(), 
    midi_program_to_instrument_name_mapper.items()
))[0][0]