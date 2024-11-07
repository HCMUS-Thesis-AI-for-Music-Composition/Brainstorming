from dto.Midi import MidiDTO
from converter.midi_dto_to_midi_file import midi_dto_to_midi_file_converter

def multiple_dtos_to_multiple_midi_file_converter(
    dtos: list[MidiDTO], 
    output_folder: str
) -> None:
    for dto in dtos:
        filepath = f"{output_folder}/{dto.instruments[0].name}.mid"

        midi_dto_to_midi_file_converter(dto, filepath)

                