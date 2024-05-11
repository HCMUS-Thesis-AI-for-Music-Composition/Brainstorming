import const.midi as mc

from dto.Midi import MidiDTO
from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.TempoChange import TempoChangeDTO

import converter.hooktheory_utils as htu

def hooktheory_json_song_part_to_midi_dto_converter(
    hooktheory_json_song_part: dict,
    tick_per_beat: int = mc.default_ticks_per_beat,
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

    for hooktheory_key_change in hooktheory_key_changes:
        root_note = hooktheory_key_change["tonic"]
        scale = hooktheory_key_change["scale"]

        if scale == mc.ScaleName.HARMONIC_MINOR:
            pass
        elif scale.lower().strip() not in [mc.ScaleName.MAJOR, mc.ScaleName.MINOR]:
            raise ValueError(f"This scale was not predefined: {scale}")
        
        key_change_time = htu.hooktheory_start_beat_to_tick_position(
            hooktheory_key_change["beat"],
            tick_per_beat
        )

        midi_dto.key_signature_changes.append(
            KeySignatureChangeDTO(
                time=key_change_time,
                key_name=f"{root_note} {scale}"
            )
        )

    for hooktheory_tempo_change in hooktheory_tempo_changes:
        tempo_change_time = htu.hooktheory_start_beat_to_tick_position(
            hooktheory_tempo_change["beat"],
            tick_per_beat
        )

        midi_dto.tempo_changes.append(
            TempoChangeDTO(
                time=tempo_change_time,
                tempo=float(hooktheory_tempo_change["bpm"])
            )
        )

    midi_dto.instruments.append(
        htu.hooktheory_json_notes_to_instr_dto(
            notes=hooktheory_json_song_part["main_data"]["notes"],
            key_signature_changes=midi_dto.key_signature_changes,
            instrument_name=htu.htc.hooktheory_default_instr_name,
            instrument_program=htu.htc.hooktheory_default_instr_program,
            ticks_per_beat=tick_per_beat,
            velocity=htu.htc.hooktheory_default_velocity
        )
    )
    
    return midi_dto