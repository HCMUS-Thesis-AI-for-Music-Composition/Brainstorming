from copy import deepcopy
from dto.Midi import MidiDTO

def multiple_instr_midi_dto_to_dtos_converter(
    midi_dto: MidiDTO
) -> list[MidiDTO]:
    single_dtos = []
    for instrument in midi_dto.instruments:
        single_dto = MidiDTO()
        single_dto.ticks_per_beat = midi_dto.ticks_per_beat
        single_dto.max_tick = midi_dto.max_tick
        single_dto.lyrics = midi_dto.lyrics
        single_dto.tempo_changes = midi_dto.tempo_changes
        single_dto.key_signature_changes = midi_dto.key_signature_changes
        single_dto.time_signature_changes = midi_dto.time_signature_changes
        single_dto.instruments = [instrument]
        single_dto.markers = midi_dto.markers

        single_dtos.append(deepcopy(single_dto))
    return single_dtos