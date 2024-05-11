from dto.TempoChange import TempoChangeDTO
from dto.KeySignatureChange import KeySignatureChangeDTO

def current_tempo_from_midi_dto_tempo_changes(
    midi_dto_tempo_changes: list[TempoChangeDTO],
    note_position: int
):
    # Sort the tempo changes by time
    midi_dto_tempo_changes = sorted(
        midi_dto_tempo_changes, 
        key = lambda tempo_change: tempo_change.time
    )
    
    for tempo_change in midi_dto_tempo_changes:
        if note_position >= tempo_change.time:
            return tempo_change.tempo
        else:
            pass

def current_key_signature_from_midi_dto_key_signature_changes(
    midi_dto_key_signature_changes: list[KeySignatureChangeDTO], 
    note_position: int
):
    # Sort the key signature changes by time
    midi_dto_key_signature_changes = sorted(
        midi_dto_key_signature_changes, 
        key = lambda key_signature_change: key_signature_change.time
    )
    
    for key_signature_change in midi_dto_key_signature_changes:
        if note_position >= key_signature_change.time:
            return key_signature_change.key_name
        else:
            pass