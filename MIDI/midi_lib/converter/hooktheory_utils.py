import re

from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.TempoChange import TempoChangeDTO
from dto.Instrument import InstrumentDTO
from dto.Note import NoteDTO

import const.hooktheory_const as htc
import const.midi as mc

from converter.note_position import position_to_tick_converter

import midi_utils as mu

def hooktheory_start_beat_to_tick_position(
    beat: float,
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat
) -> int:
    return position_to_tick_converter(
        position=beat - 1,
        tick_per_beat=ticks_per_beat,
        position_resolution=1
    )

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
    return (
        hooktheory_start_beat_to_tick_position(
            hooktheory_start_beat,
            ticks_per_beat
        ) + hooktheory_duration_to_tick_duration(
            hooktheory_duration,
            ticks_per_beat
        )
    )

def scale_degree_to_midi_note_number(
    scale_degree_str: str,
    key: htc.HookTheoryKeySignatureDTO,
    octave: int = 0
):
    # Check if scale degree is n, bn or #n
    accidental_semitones = 0

    if re.match(r"^\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str)
    elif re.match(r"^b\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str[1:])
        accidental_semitones = -1
    elif re.match(r"^\#\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str[1:])
        accidental_semitones = 1

    root_midi_note_number = mc.inversed_based_midi_note_numbers[key.root_note_str]
    scale_formula = mc.scale_formulas[key.scale_name]
    
    base_midi_note = root_midi_note_number + sum(
        scale_formula[:(scale_degree - 1)]
    ) + accidental_semitones
    
    return base_midi_note + 12 * octave + mc.C4_midi_note_number

def key_signature_str_to_hooktheory_key_signature_dto(
    key_sig_str: str
) -> htc.HookTheoryKeySignatureDTO:
    """
        Converts a key signature string to a HookTheoryKeySignatureDTO object.

        key_sig_str: str
            The key signature string to convert.

            Example: "C major", "F# minor", "Bb major", "Eb minor"
    """
    key_sig_str = key_sig_str.replace(" ", "")
    
    if "b" in key_sig_str or "#" in key_sig_str:
        key_sig_str = f"{key_sig_str[0:2]} {key_sig_str[2:]}"
    else:
        key_sig_str = f"{key_sig_str[0:1]} {key_sig_str[1:]}"
    
    key_str_parts = key_sig_str.split(" ")

    root_note_str = key_str_parts[0]
    scale = key_str_parts[1]

    return htc.HookTheoryKeySignatureDTO(
        root_note_str=root_note_str,
        scale=scale
    )

def hooktheory_json_note_to_note_dto(
    note: dict,
    key_signature_changes: list[KeySignatureChangeDTO],
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat,
    velocity: int = htc.hooktheory_default_velocity
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

    key_name_str: htc.HookTheoryKeySignatureDTO = mu.current_key_signature_from_midi_dto_key_signature_changes(
        key_signature_changes,
        note_start_tick
    )

    key = key_signature_str_to_hooktheory_key_signature_dto(
        key_name_str
    )
    
    return NoteDTO(
        start=note_start_tick,
        end=note_end_tick,
        pitch=scale_degree_to_midi_note_number(
            note["sd"],
            key,
            octave=note["octave"]
        ),
        velocity=velocity
    )

def hooktheory_json_key_change_to_key_signature_changes_dto_converter(
    hooktheory_key_changes: list[dict],
    tick_per_beat: int = mc.default_ticks_per_beat
) -> list[KeySignatureChangeDTO]:
    key_signature_changes = []

    for hooktheory_key_change in hooktheory_key_changes:
        root_note = hooktheory_key_change["tonic"]
        scale = hooktheory_key_change["scale"]

        if scale == mc.ScaleName.HARMONIC_MINOR:
            pass
        elif scale.lower().strip() not in [mc.ScaleName.MAJOR, mc.ScaleName.MINOR]:
            raise ValueError(f"This scale was not predefined: {scale}")
        
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