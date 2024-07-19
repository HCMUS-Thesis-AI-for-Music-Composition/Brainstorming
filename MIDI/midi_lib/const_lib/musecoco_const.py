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

# FOR DATA AUGMENTATION
required_substring_for_attributes: dict[str, list[str]] = {
    "I1_1" : ["[INSTRUMENTS]"],
    "I1_0" : ["[INSTRUMENTS]"],
    "P4_1" : ["[RANGE]"],
    "C1_0" : ["bright", 'radiant', 'shining', 'luminous', 'vivid', 'brilliant', 'dazzling', 'beaming', 'glowing', 'sparkling', 'sunny', 'cheerful', 'optimistic', 'happy', 'joyful', 'lively', 'colorful'],
    "C1_1" : ["gloomy", 'melancholy', 'somber', 'depressing', 'miserable', 'dismal', 'bleak', 'desolate', 'sorrowful', 'morose', 'dark', 'dreary', 'funereal', 'disheartening', 'cheerless', 'despairing'],
    "C1_2" : ["start", "turn", "begin"],
    "C1_3" : ["start", "turn", "begin"],
    "R1_1" : ["dance", "dancing", "dancer", "dances", "danced"],
    "R1_0" : ["dance", "dancing", "dancer", "dances", "danced"],
    "R3_1" : ["strong", "powerful", "vigorous", "forceful", "potent", "intense", "robust", "sturdy", "solid", "stalwart", "resilient", "tough", "hardy", "hearty", "stout"],
    "R3_0" : ["calm", "peaceful", "tranquil", "serene", "placid", "quiet", "still", "gentle", "mild", "soft", "soothing", "relaxing", "restful", "untroubled", "undisturbed"],
    "R3_2" : ["moderate", "medium", "average", "middling", "intermediate", "mediocre", "ordinary", "common", "fair", "tolerable", "passable", "adequate", "acceptable", "satisfactory", "reasonable"],
    "S4_1" : ["[GENRE]"],
    "S4_0" : ["[GENRE]"],
    "S2_1" : ["[ARTIST]"],
    "S2_0" : ["[ARTIST]"],
    "B1_1" : ["[NUM_BARS]"],
    "TS1_1" : ["[TIME_SIGNATURE]"],
    "TS1_o" : ["uncommon", "rare", "unique", "exceptional", "extraordinary", "unusual", "singular", "peculiar", "curious", "odd", "strange", "weird", "bizarre", "abnormal", "atypical"],
    "K1_1" : ["[KEY]"],
    "T1_0" : ["fast", "quick", "swift", "speedy", "rapid", "brisk", "hasty", "nimble", "fleet", "snappy", "prompt", "expeditious", "immediate", "sudden", "hurried"],
    "T1_1" : ["slow", "sluggish", "lethargic", "lazy", "lackadaisical", "listless", "torpid", "dull", "unhurried", "unrushed", "leisurely", "easy", "relaxed", "comfortable", "plodding"],
    "T1_2" : ["moderate", "medium", "average", "middling", "intermediate", "mediocre", "ordinary", "common", "fair", "tolerable", "passable", "adequate", "acceptable", "satisfactory", "reasonable"],
    "EM1_1" : ["[EMOTION]"],
    "TM1_1" : ["[TM1]"]
}
    
required_substring_for_positive_and_negative_attributes: dict[str, list[str]] = {
    "I1_0" : ["n't", "not", "unsuitable", "inappropriate", "doesn't"],
    "R1_1" : ["suit", "perfect", "great"],
    "R1_0" : ["n't", "not", "unsuitable", "inappropriate", "doesn't"],
    "S4_0" : ["doesn't", "not", "unfit", "unsuitable", "inappropriate"],
    "S2_0" : ["doesn't", "not", "unfit", "unsuitable", "inappropriate"],
}