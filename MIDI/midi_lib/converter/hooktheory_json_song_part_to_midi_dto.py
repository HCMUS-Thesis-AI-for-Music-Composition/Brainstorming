import random
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

    # Key Signature Changes
    midi_dto.key_signature_changes = htu.hooktheory_json_key_change_to_key_signature_changes_dto_converter(
        hooktheory_key_changes,
        tick_per_beat
    )

    # Tempo Changes
    midi_dto.tempo_changes = htu.hooktheory_json_tempo_change_to_tempo_change_dto_converter(
        hooktheory_tempo_changes,
        tick_per_beat
    )

    # Time Signature/Meter Changes
    midi_dto.time_signature_changes = htu.hooktheory_json_meter_change_to_time_signature_change_dto_converter(
        hooktheory_json_song_part["main_data"]["meters"],
        tick_per_beat
    )

    # Random a melody instrument
    melody_instrument_program = htu.htc.hooktheory_default_melody_instrument_programs[
        random.randint(0, len(htu.htc.hooktheory_default_melody_instrument_programs) - 1)
    ]

    melody_instrument_name = mc.midi_program_to_instrument_name_mapper[melody_instrument_program]

    melody_instrument_name = f"{melody_instrument_name} - Melodies"

    # Random a chord instrument
    chord_instrument_program = htu.htc.hooktheory_default_chord_instrument_programs[
        random.randint(0, len(htu.htc.hooktheory_default_chord_instrument_programs) - 1)
    ]

    chord_instrument_name = mc.midi_program_to_instrument_name_mapper[chord_instrument_program]

    chord_instrument_name = f"{chord_instrument_name} - Chords"

    midi_dto.instruments.append(
        hooktheory_json_notes_to_instr_dto_converter(
            notes=hooktheory_json_song_part["main_data"]["notes"],
            key_signature_changes=midi_dto.key_signature_changes,
            instrument_name=melody_instrument_name,
            instrument_program=melody_instrument_program,
            ticks_per_beat=tick_per_beat,
            velocity=velocity
        )
    )

    midi_dto.instruments.append(
        hooktheory_json_chords_to_instrument_dto_converter(
            chords=hooktheory_json_song_part["main_data"]["chords"],
            key_signature_changes=midi_dto.key_signature_changes,
            instrument_name=chord_instrument_name,
            instrument_program=chord_instrument_program,
            ticks_per_beat=tick_per_beat,
            velocity=(velocity - htu.htc.velocity_delta)
        )
    )
    
    return midi_dto