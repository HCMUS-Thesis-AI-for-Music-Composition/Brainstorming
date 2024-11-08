from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.TimeSignatureChange import TimeSignatureChangeDTO
from dto.TimeSignature import TimeSignatureDTO
from dto.TempoChange import TempoChangeDTO
from dto.Note import NoteDTO

import const.hooktheory_const as htc
import const.midi as mc

from converter.note_position import position_to_tick_converter

import midi_utils as mu

def hooktheory_start_beat_to_tick_position(
    beat: float,
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat,
) -> int:
    tick_position = None
    
    if beat >= 1:
        tick_position = position_to_tick_converter(
            position=beat - 1,
            tick_per_beat=ticks_per_beat,
            position_resolution=1
        ) 
    elif beat >= 0 and beat < 1:
        print(
            f"WARNING: hooktheory_start_beat_to_tick_position: beat = {beat} is less than 1."
        )
    else:
        pass

    return tick_position

def hooktheory_duration_to_tick_duration(
    duration: float,
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat
) -> int:
    return position_to_tick_converter(
        position=duration,
        tick_per_beat=ticks_per_beat,
        position_resolution=1
    )

def calculate_note_end_tick_position(
    hooktheory_start_beat: float,
    hooktheory_duration: float,
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat
) -> int:
    start_tick = hooktheory_start_beat_to_tick_position(
        hooktheory_start_beat,
        ticks_per_beat
    )
    
    tick_duration = hooktheory_duration_to_tick_duration(
        hooktheory_duration,
        ticks_per_beat
    )

    if start_tick == None or tick_duration == None:
        return None
    else:
        return start_tick + tick_duration

def hooktheory_json_note_to_note_dto(
    note: dict,
    key_signature_changes: list[KeySignatureChangeDTO],
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat,
    velocity: int = htc.hooktheory_default_velocity,
) -> NoteDTO:
    note_start_tick = hooktheory_start_beat_to_tick_position(
        note["beat"],
        ticks_per_beat
    )

    note_end_tick = calculate_note_end_tick_position(
        note["beat"],
        note["duration"],
        ticks_per_beat
    )

    if note_start_tick == None or note_end_tick == None:
        return None
    else:
        pass

    key_name_str: str = mu.current_key_signature_from_midi_dto_key_signature_changes(
        key_signature_changes,
        note_start_tick
    )

    key = mu.key_signature_str_to_key_signature_dto(
        key_name_str
    )
    
    note_dto = NoteDTO(
        start=note_start_tick,
        end=note_end_tick,
        pitch=mu.scale_degree_to_midi_note_number(
            note["sd"],
            key_signature=key,
            octave=note["octave"]
        ),
        velocity=velocity
    )
    
    return note_dto

def hooktheory_json_key_change_to_key_signature_changes_dto_converter(
    hooktheory_key_changes: list[dict],
    tick_per_beat: int = mc.default_ticks_per_beat,
) -> list[KeySignatureChangeDTO]:
    key_signature_changes = []

    for hooktheory_key_change in hooktheory_key_changes:
        root_note = hooktheory_key_change["tonic"]
        scale = hooktheory_key_change["scale"]

        if scale not in mc.scale_formulas.keys():
            raise ValueError(
                f"hooktheory_json_key_change_to_key_signature_changes_dto_converter: This scale was not predefined: {scale}"
            )
        else:
            pass
        
        key_change_time = hooktheory_start_beat_to_tick_position(
            hooktheory_key_change["beat"],
            tick_per_beat
        )

        key_signature_changes.append(
            KeySignatureChangeDTO(
                time=key_change_time,
                key_name=f"{root_note} {scale}"
            )
        )

    return key_signature_changes

def hooktheory_json_tempo_change_to_tempo_change_dto_converter(
    hooktheory_tempo_changes: list[dict],
    tick_per_beat: int = mc.default_ticks_per_beat
) -> list[TempoChangeDTO]:
    tempo_changes = []

    for hooktheory_tempo_change in hooktheory_tempo_changes:
        tempo_change_time = hooktheory_start_beat_to_tick_position(
            hooktheory_tempo_change["beat"],
            tick_per_beat
        )

        tempo_changes.append(
            TempoChangeDTO(
                time=tempo_change_time,
                tempo=float(hooktheory_tempo_change["bpm"])
            )
        )

    return tempo_changes

def hooktheory_json_meter_change_to_time_signature_change_dto_converter(
    hooktheory_meter_changes: list[dict],
    tick_per_beat: int = mc.default_ticks_per_beat
) -> list[TimeSignatureChangeDTO]:
    time_signature_changes = []

    for hooktheory_meter_change in hooktheory_meter_changes:
        meter_change_time = hooktheory_start_beat_to_tick_position(
            hooktheory_meter_change["beat"],
            tick_per_beat
        )

        numBeats = hooktheory_meter_change["numBeats"]
        beatUnit = hooktheory_meter_change["beatUnit"]

        numerator = int(numBeats)
        denominator = htc.beat_unit_to_time_signature_denominator_mapper[
            int(beatUnit)
        ]

        time_signature_changes.append(
            TimeSignatureChangeDTO(
                time=meter_change_time,
                time_signature=TimeSignatureDTO(
                    numerator=numerator,
                    denominator=denominator
                )
            )
        )

    return time_signature_changes