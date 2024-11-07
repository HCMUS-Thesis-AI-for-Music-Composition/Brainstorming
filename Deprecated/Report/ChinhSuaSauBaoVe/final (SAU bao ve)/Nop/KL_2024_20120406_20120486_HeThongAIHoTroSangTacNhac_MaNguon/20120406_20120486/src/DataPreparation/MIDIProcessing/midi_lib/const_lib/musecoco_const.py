# from musecoco_utils import generate_time_signature_dict

str_abbr_bar = "b"
str_abbr_time_signature = "s"
str_abbr_instrument = "i"
str_abbr_duration = "d"
str_abbr_pitch_name = "n"
str_abbr_family = "f"
str_abbr_position = "o"
str_abbr_tempo = "t"
str_abbr_pitch = "p"
str_abbr_velocity = "v"
str_abbr_pitch_octave = "c"
str_abbr_special = "e"

max_ts_denominator_power = 6
max_notes_per_bar = 2

pos_resolution = 12
max_duration = 8
musecoco_default_ticks_per_beat = 480

# musecoco_time_signature_mapper = generate_time_signature_dict(
#     max_ts_denominator_power=max_ts_denominator_power,
#     max_notes_per_bar=max_notes_per_bar
# )

# time_signature: 8
# position: 0     tempo: 35    instrument: 0     pitch: 64 E4   duration: 11    velocity: 20    pitch: 43 G2   duration: 11    velocity: 20
# position: 6     tempo: 35    instrument: 0     pitch: 74 D5   duration: 12    velocity: 20    pitch: 52 E3   duration: 6     velocity: 20    pitch: 48 C3   duration: 6     velocity: 20
# position: 24    tempo: 35    instrument: 0     pitch: 72 C5   duration: 12    velocity: 20    instrument: 58    pitch: 43 G2   duration: 12    velocity: 20    pitch: 59 B3   duration: 12    velocity: 20    pitch: 53 F3   duration: 3     velocity: 20    bar: 1
# time_signature: 8

next_acceptable_keys: dict = {
    "s": ["b", "o"],
    "o": ["t"],
    "t": ["i"],
    "i": ["p"],
    "p": ["d"],
    "d": ["v"],
    "v": ["i", "b", "p", "o"],
    "b": ["s"],
}
