from dto.Note import NoteDTO
from dto.Chord import ChordDTO

import const.midi as mc

def chord_dto_to_note_dtos_converter(chord_dto: ChordDTO) -> list[NoteDTO]:
    """
        Convert a ChordDTO to a list of NoteDTOs
    """
    notes = []
    
    scale_formula = mc.scale_formulas[chord_dto.key_signature.scale_name]

    root = chord_dto.root

    
    return notes