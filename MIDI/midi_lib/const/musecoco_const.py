from musecoco_utils import generate_time_signature_dict

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

musecoco_time_signature_mapper = generate_time_signature_dict(
    max_ts_denominator_power=max_ts_denominator_power, 
    max_notes_per_bar=max_notes_per_bar
)