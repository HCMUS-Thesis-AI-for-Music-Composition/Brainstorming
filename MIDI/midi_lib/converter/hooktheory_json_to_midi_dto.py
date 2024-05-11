import const.midi as mc

from dto.Midi import MidiDTO

import converter.hooktheory_utils as htu
from converter.hooktheory_json_chords_to_instrument_dto import hooktheory_json_chords_to_instrument_dto_converter
from converter.hooktheory_json_notes_to_instr_dto import hooktheory_json_notes_to_instr_dto_converter

def hooktheory_json_song_part_to_midi_dto_converter(
    hooktheory_json_song_part: dict,
    tick_per_beat: int = mc.default_ticks_per_beat,
    velocity: int = mc.default_velocity
) -> MidiDTO:
    midi_dto = MidiDTO()
    
    midi_dto.ticks_per_beat = tick_per_beat
    midi_dto.max_tick = 0
    midi_dto.lyrics = ""
    midi_dto.tempo_changes = []
    midi_dto.key_signature_changes = []
    midi_dto.time_signature_changes = []
    midi_dto.instruments = []
    midi_dto.markers = []
    
    hooktheory_key_changes = hooktheory_json_song_part["main_data"]["keys"]
    hooktheory_tempo_changes = hooktheory_json_song_part["main_data"]["tempos"]

    midi_dto.key_signature_changes = htu.hooktheory_json_key_change_to_key_signature_changes_dto_converter(
        hooktheory_key_changes,
        tick_per_beat
    )

    midi_dto.tempo_changes = htu.hooktheory_json_tempo_change_to_tempo_change_dto_converter(
        hooktheory_tempo_changes,
        tick_per_beat
    )

    midi_dto.instruments.append(
        hooktheory_json_notes_to_instr_dto_converter(
            notes=hooktheory_json_song_part["main_data"]["notes"],
            key_signature_changes=midi_dto.key_signature_changes,
            instrument_name=htu.htc.hooktheory_default_instr_name,
            instrument_program=htu.htc.hooktheory_default_instr_program,
            ticks_per_beat=tick_per_beat,
            velocity=velocity
        )
    )

    midi_dto.instruments.append(
        hooktheory_json_chords_to_instrument_dto_converter(
            chords=hooktheory_json_song_part["main_data"]["chords"],
            key_signature_changes=midi_dto.key_signature_changes,
            instrument_name=htu.htc.hooktheory_default_instr_name,
            instrument_program=htu.htc.hooktheory_default_instr_program,
            ticks_per_beat=tick_per_beat,
            velocity=velocity
        )
    )
    
    return midi_dto