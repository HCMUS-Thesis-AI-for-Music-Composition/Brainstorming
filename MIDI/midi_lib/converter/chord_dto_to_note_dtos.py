from dto.Note import NoteDTO
from dto.Chord import ChordDTO

import const.midi as mc
import const.hooktheory_const as htc

def chord_dto_to_note_dtos_converter(chord_dto: ChordDTO) -> list[NoteDTO]:
    """
        Convert a ChordDTO to a list of NoteDTOs
    """
    chord_voice_accidentals = {
        chord_voice : None
        for chord_voice in range(1, mc.default_max_chord_voice_degree + 1)
    }
    
    scale_formula = mc.scale_formulas[chord_dto.key_signature.scale_name]

    root = chord_dto.root

    n_note_based_on_type = (chord_dto.type - 1) / 2
    for note_idx in range(1, n_note_based_on_type + 1):
        chord_voice_accidentals[note_idx] = mc.Accidental.NATURAL


    return []