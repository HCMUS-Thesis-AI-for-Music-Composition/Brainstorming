from dto.Instrument import InstrumentDTO
from dto.KeySignatureChange import KeySignatureChangeDTO

import const.hooktheory_const as htc
import converter.hooktheory_utils as htu

def hooktheory_json_notes_to_instr_dto_converter(
    notes: list[dict],
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

    for note in notes:
        if note["isRest"]:
            pass
        else:
            instrument.notes.append(
                htu.hooktheory_json_note_to_note_dto(
                    note,
                    key_signature_changes,
                    ticks_per_beat,
                    velocity
                )
            )

    return instrument