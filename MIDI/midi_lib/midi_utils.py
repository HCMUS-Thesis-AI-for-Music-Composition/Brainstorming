from dto.TempoChange import TempoChangeDTO

def current_tempo_from_midi_dto_tempo_changes(midi_dto_tempo_changes: TempoChangeDTO, note_position: int):
    for tempo_change in midi_dto_tempo_changes:
        if note_position >= tempo_change.time:
            return tempo_change.tempo
        else:
            pass