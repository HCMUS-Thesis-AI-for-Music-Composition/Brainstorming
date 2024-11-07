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
    "I1_1" : ["[INSTRUMENTS]", "instrument"],
    "I1_0" : ["[INSTRUMENTS]", "instrument"],
    "P4_1" : ["[RANGE]", "range"],
    "C1_0" : ["bright", 'radiant', 'shining', 'luminous', 'vivid', 'brilliant', 'dazzling', 'beaming', 'glowing', 'sparkling', 'sunny', 'cheerful', 'optimistic', 'happy', 'happiness', 'joy', 'lively', 'colorful', 'bliss'],
    "C1_1" : ["gloomy", 'melancholy', 'melancholic', 'somber', 'depressing', 'miserable', 'dismal', 'bleak', 'desolate', 'sorrowful', 'morose', 'dark', 'dreary', 'funereal', 'disheartening', 'cheerless', 'despairing', 'sad'],
    "C1_2" : ["start", "turn", "begin"],
    "C1_3" : ["start", "turn", "begin"],
    "R1_1" : ["dance", "dancing", "dancer", "dances", "danced"],
    "R1_0" : ["dance", "dancing", "dancer", "dances", "danced"],
    "R3_0" : ["beat", "rhythm", "tempo", "effect on my mind", "effect", "pace"],
    "R3_1" : ["beat", "rhythm", "tempo", "effect on my mind", "effect", "pace"],
    "R3_2" : ["beat", "rhythm", "tempo", "effect on my mind", "effect", "pace"],
    "S4_1" : ["[GENRE]", "genre"],
    "S4_0" : ["[GENRE]", "genre"],
    "S2_1" : ["[ARTIST]", "artist"],
    "S2_0" : ["[ARTIST]", "artist"],
    "B1_1" : ["[NUM_BARS]", "bar"],
    "T1_0" : ["tempo", "bpm", "beats per minute", "rate", "speed", "pace", "pulse", "rhythm", "is", "move"],
    "T1_1" : ["tempo", "bpm", "beats per minute", "rate", "speed", "pace", "pulse", "rhythm", "is", "move"],
    "T1_2" : ["tempo", "bpm", "beats per minute", "rate", "speed", "pace", "pulse", "rhythm", "is", "move"],
    "TS1_1" : ["[TIME_SIGNATURE]", "time signature"],
    "TS1_o" : ["uncommon", "rare", "unique", "exceptional", "extraordinary", "unusual", "singular", "peculiar", "curious", "odd", "strange", "weird", "bizarre", "abnormal", "atypical", "not", "non", "deviate", "deviating", "unconventional", "out of the norm", "out of", "out-of"],
    "K1_1" : ["[KEY]", "key"],
    "EM1_1" : ["[EMOTION]", "emotion"],
    "TM1_1" : ["[TM1]", "seconds", "minute"],
    "I4_1" : "instrument"
}
    
required_substring_for_positive_and_negative_attributes: dict[str, list[str]] = {
    "R3_1" : ["strong", "powerful", "vigorous", "forceful", "potent", "intense", "robust", "sturdy", "solid", "stalwart", "resilient", "tough", "hardy", "hearty", "stout", "energetic", "vital", "lively", "high energy", "high spirited", "high powered", "high octane", "high voltage", "high intensity", "high impact", "high performance", "high speed", "high velocity", "high power", "high strength", "high endurance", "high resilience", "high toughness", "high hardiness", "high heartiness", "high stoutness", "high vitality", "high liveliness", "invigorating", "exhilarating", "stimulating"],
    "R3_0" : ["calm", "peaceful", "tranquil", "serene", "placid", "quiet", "still", "gentle", "mild", "soft", "soothing", "relaxing", "restful", "untroubled", "undisturbed", "comfort", "lulling"],
    "R3_2" : ["moderate", "medium", "average", "middling", "intermediate", "mediocre", "ordinary", "common", "fair", "tolerable", "passable", "adequate", "acceptable", "satisfactory", "reasonable", "neither too fast nor too slow", "neither", "not too"],
    "T1_0" : ["fast", "quick", "swift", "speedy", "rapid", "brisk", "hasty", "nimble", "fleet", "snappy", "prompt", "expeditious", "immediate", "sudden", "hurried"],
    "T1_1" : ["slow", "sluggish", "lethargic", "lazy", "lackadaisical", "listless", "torpid", "dull", "unhurried", "unrushed", "leisurely", "easy", "relaxed", "comfortable", "plodding", "low"],
    "T1_2" : ["moderate", "medium", "average", "middling", "intermediate", "mediocre", "ordinary", "common", "fair", "tolerable", "passable", "adequate", "acceptable", "satisfactory", "reasonable", "meditative"],
    "I4_0" : ["exclude", "won", "n't", "not", "non", "unsuitable", "inappropriate", "doesn't", "excluded", "excludes", "excluding", "exclude", "exclusion", "exclusively", "exclusive", "exclusivity", "exception", "exceptional", "exceptionally"],
    "I4_1" : ["primary", "main", "chief", "principal", "leading", "foremost", "first", "premier", "major", "dominant", "central", "key", "crucial", "vital", "paramount", "essential", "fundamental", "basic", "important", "significant", "substantial", "considerable", "notable", "noteworthy", "remarkable", "outstanding", "prominent", "eminent", "distinguished", "preeminent", "superior", "supreme", "top", "topmost", "uppermost", "highest", "greatest", "utmost", "maximum", "maximal", "max", "extreme", "intense", "severe", "acute", "excessive", "exorbitant", "extensive", "comprehensive", "complete", "total", "absolute", "outright", "unqualified", "unconditional", "unreserved", "unmitigated", "unlimited", "unrestricted"],
    "I1_0" : ["exclude", "won", "n't", "not", "non", "unsuitable", "inappropriate", "doesn't", "excluded", "excludes", "excluding", "exclude", "exclusion", "exclusively", "exclusive", "exclusivity", "exception", "exceptional", "exceptionally"],
    "R1_1" : ["suit", "perfect", "great"],
    "R1_0" : ["n't", "not", "unsuitable", "inappropriate", "doesn't", "non"],
    "S4_0" : ["doesn't", "not", "unfit", "unsuitable", "inappropriate", "non"],
    "S2_0" : ["doesn't", "not", "unfit", "unsuitable", "inappropriate", "non"],
}