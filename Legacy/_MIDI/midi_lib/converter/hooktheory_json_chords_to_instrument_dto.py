from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.Instrument import InstrumentDTO

import const.hooktheory_const as htc

from converter.hooktheory_json_chord_to_chord_dto import hooktheory_json_chord_to_chord_dto_converter
from converter.chord_dto_to_note_dtos import chord_dto_to_note_dtos_converter

def hooktheory_json_chords_to_instrument_dto_converter(
    chords: list[dict],
    key_signature_changes: list[KeySignatureChangeDTO],
    instrument_name: str,
    instrument_program: int,
    ticks_per_beat: int = htc.hooktheory_ticks_per_beat,
    velocity: int = htc.hooktheory_default_velocity
) -> InstrumentDTO:
    instrument = InstrumentDTO(
        program=instrument_program,
        name=instrument_name
    )

    for chord in chords:
        if chord["isRest"]:
            continue
        
        chord_dto = hooktheory_json_chord_to_chord_dto_converter(
            chord,
            key_signature_changes,
            ticks_per_beat,
            velocity
        )
        
        instrument.notes.extend(
            chord_dto_to_note_dtos_converter(chord_dto)
        )

    return instrument