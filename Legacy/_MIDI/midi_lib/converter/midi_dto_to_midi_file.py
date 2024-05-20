from dto.Midi import MidiDTO
from midi_file_utils import write_midi_file
from converter.midi_dto_to_midi_file_object import midi_dto_to_midi_file_object_converter

def midi_dto_to_midi_file_converter(
    midi_dto: MidiDTO, 
    filepath: str
) -> None:
    midi_obj = midi_dto_to_midi_file_object_converter(midi_dto)

    write_midi_file(midi_obj, filepath)