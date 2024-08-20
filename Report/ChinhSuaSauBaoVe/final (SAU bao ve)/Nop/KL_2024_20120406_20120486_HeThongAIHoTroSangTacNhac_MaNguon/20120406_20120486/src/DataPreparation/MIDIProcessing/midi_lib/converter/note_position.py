from const_lib.midi_const import default_ticks_per_beat, default_position_resolution

def position_to_tick_converter(
    position, 
    tick_per_beat=default_ticks_per_beat, 
    position_resolution=default_position_resolution
):
    return round(position * tick_per_beat / position_resolution)

def tick_to_position_converter(
    tick, 
    tick_per_beat=default_ticks_per_beat, 
    position_resolution=default_position_resolution
):
    return round(tick * position_resolution / tick_per_beat)
    