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
    root_scale_degree = hooktheory_json_chord["root"]

    if type(root_scale_degree) == int:
        pass
    elif type(root_scale_degree) == str:
        if root_scale_degree.isdigit():
            root_scale_degree = int(root_scale_degree)
        else:
            raise ValueError(
                f"ERROR: hooktheory_json_chord_to_chord_dto_converter: root_scale_degree is not a digit: {root_scale_degree}"
            )

    start_beat = hooktheory_json_chord["beat"]
    duration = None

    if start_beat >= 1:
        duration = hooktheory_json_chord["duration"]
    elif start_beat < 1 and start_beat >= 0:
        duration = hooktheory_json_chord["duration"] - start_beat
        start_beat = 1

        print(
            f"WARNING: hooktheory_json_chord_to_chord_dto_converter: 0 < start_beat < 1: {start_beat}"
        )

    start_tick = htu.hooktheory_start_beat_to_tick_position(
        start_beat,
        ticks_per_beat
    )
    
    end_tick = htu.calculate_note_end_tick_position(
        start_beat,
        duration,
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

    # MESSAGE
    if hooktheory_json_chord["applied"] is not None and borrowed is not None:
        if hooktheory_json_chord["applied"] != 0 and borrowed != [] and borrowed != "":
            print(
                f"hooktheory_json_chord_to_chord_dto_converter: Message: applied and borrowed chords are not mutually exclusive:\n    -> {hooktheory_json_chord}"
            )

    alternate = None
    
    if "alternate" in hooktheory_json_chord:
        alternate = hooktheory_json_chord["alternate"] 
    else:
        alternate = None
    
    return ChordDTO(
        key_signature=key_sig,
        root=root_scale_degree,
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
        alternate=alternate,
        borrowed=borrowed,
        velocity=velocity
    )
