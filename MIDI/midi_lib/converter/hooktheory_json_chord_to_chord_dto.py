from dto.Chord import ChordDTO
from dto.KeySignature import KeySignatureDTO
from dto.KeySignatureChange import KeySignatureChangeDTO

import const.hooktheory_const as htc
import const.midi as mc

import midi_utils as mu
import converter.hooktheory_utils as htu

def hooktheory_json_chord_to_chord_dto_converter(
    hooktheory_json_chord: dict,
    key_signature_changes: list[KeySignatureChangeDTO],
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat,
    velocity: int = htc.hooktheory_default_velocity
) -> ChordDTO:
    """
        Convert a HookTheory JSON chord to a ChordDTO
    """
    start_tick = htu.hooktheory_start_beat_to_tick_position(
        hooktheory_json_chord["beat"],
        ticks_per_beat
    )
    
    end_tick = htu.calculate_note_end_tick_position(
        hooktheory_json_chord["beat"],
        hooktheory_json_chord["duration"],
        ticks_per_beat
    )

    key_sig = mu.current_key_signature_from_midi_dto_key_signature_changes(
        key_signature_changes,
        start_tick
    )

    key_sig = key_sig.split(" ")

    root_note_str = key_sig[0]

    scale_name = key_sig[1]

    key_sig = KeySignatureDTO(
        tonic_midi_note_number=mc.inversed_based_midi_note_numbers[
            root_note_str
        ],
        scale_name=scale_name
    )

    borrowed = [] if (
        hooktheory_json_chord["borrowed"] is None
    ) else hooktheory_json_chord["borrowed"]

    return ChordDTO(
        key_signature=key_sig,
        root=hooktheory_json_chord["root"],
        start=start_tick,
        end=end_tick,
        type=hooktheory_json_chord["type"],
        inversion=hooktheory_json_chord["inversion"],
        applied=hooktheory_json_chord["applied"],
        adds=hooktheory_json_chord["adds"],
        omits=hooktheory_json_chord["omits"],
        alterations=hooktheory_json_chord["alterations"],
        suspensions=hooktheory_json_chord["suspensions"],
        pedal=[],
        alternate=hooktheory_json_chord["alternate"],
        borrowed=borrowed,
        velocity=velocity
    )
