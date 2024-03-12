from dto.Note import NoteDTO
from dto.TempoChange import TempoChangeDTO
from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.TimeSignatureChange import TimeSignatureChangeDTO
from dto.Instrument import InstrumentDTO
from dto.Midi import MidiDTO
from dto.Marker import MarkerDTO
from miditoolkit import MidiFile
import numpy as np


def midi_data_to_midi_dto_converter(midi_data: MidiFile) -> MidiDTO:
    midi_dto = MidiDTO()
    
    midi_dto.ticks_per_beat = midi_data.ticks_per_beat
    midi_dto.max_tick = midi_data.max_tick
    midi_dto.lyrics = midi_data.lyrics

    for tempo_change in midi_data.tempo_changes:
        midi_dto.tempo_changes.append(
            TempoChangeDTO(
                time=tempo_change.time,
                tempo=tempo_change.tempo
            )
        )

    for key_signature_change in midi_data.key_signature_changes:
        midi_dto.key_signature_changes.append(
            KeySignatureChangeDTO(
                time=key_signature_change.time,
                key_name=key_signature_change.key_name
            )
        )

    for time_signature_change in midi_data.time_signature_changes:
        midi_dto.time_signature_changes.append(
            TimeSignatureChangeDTO(
                time=time_signature_change.time,
                numerator=time_signature_change.numerator,
                denominator=time_signature_change.denominator
            )
        )

    for instrument in midi_data.instruments:
        instrument_info = InstrumentDTO(
            name=instrument.name,
            program=np.int8(instrument.program).item(),
            notes=[]
        )

        for note in instrument.notes:
            instrument_info.notes.append(
                NoteDTO(
                    start=note.start,
                    end=note.end,
                    pitch=note.pitch,
                    velocity=note.velocity
                )
            )

        midi_dto.instruments.append(instrument_info)
    
    for marker in midi_data.markers:
        midi_dto.markers.append(
            MarkerDTO(
                time=marker.time,
                text=marker.text
            )
        )

    return midi_dto