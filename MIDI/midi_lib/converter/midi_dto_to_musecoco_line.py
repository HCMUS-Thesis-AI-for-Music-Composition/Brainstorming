from dto.Midi import MidiDTO
from dto.Instrument import InstrumentDTO
from dto.Note import NoteDTO
from dto.TimeSignatureChange import TimeSignatureChangeDTO
from midi_utils import beat_to_tick, musecoco_abbreviations, musecoco_abbreviations_reversed

def musecoco_line_to_midi_dto_converter(musecoco_line) -> MidiDTO:
    midi_dto = MidiDTO()

    midi_dto.ticks_per_beat = 960
    midi_dto.max_tick = 30721
    midi_dto.time_signature_changes = [
        TimeSignatureChangeDTO(
            time = 0,
            numerator = 4,
            denominator = 4
        )
    ]

    current_position = 0
    current_duration = 0
    current_pitch = 0
    current_velocity = 0
    current_instrument = 0

    midi_dto.instruments = []

    for pair in musecoco_line:
        key = list(pair.keys())[0]
        value = pair[key]

        if musecoco_abbreviations[key] == "position":
            current_position = int(value)
        elif musecoco_abbreviations[key] == "pitch":
            current_pitch = int(value)
        elif musecoco_abbreviations[key] == "duration":
            current_duration = int(value)
        elif musecoco_abbreviations[key] == "velocity":
            current_velocity = int(value)
        elif musecoco_abbreviations[key] == "instrument":
            current_instrument = int(value)

        if musecoco_abbreviations[key] == "velocity":        
            note = NoteDTO(
                start = beat_to_tick(current_position, midi_dto.ticks_per_beat),
                end = beat_to_tick(current_position + current_duration, midi_dto.ticks_per_beat),
                pitch = current_pitch,
                velocity = current_velocity
            )

            if current_instrument not in [instrument.name for instrument in midi_dto.instruments]:
                instrument = InstrumentDTO(
                    name = str(current_instrument),
                    program = 0,
                    notes = [note]
                )
                
                midi_dto.instruments.append(instrument)
            else:
                for i in range(len(midi_dto.instruments)):
                    if midi_dto.instruments[i].name == current_instrument:
                        midi_dto.instruments[i].notes.append(note)
                        break

    return midi_dto

def midi_dto_to_musecoco_line_converter(midi_dto: MidiDTO):
    musecoco_line = []

    for instrument in midi_dto.instruments:
        for note in instrument.notes:
            musecoco_line.append(
                {
                    musecoco_abbreviations_reversed["position"]: str(tick_to_beat(note.start, midi_dto.ticks_per_beat)),
                    musecoco_abbreviations_reversed["pitch"]: str(note.pitch),
                    musecoco_abbreviations_reversed["duration"]: str(tick_to_beat(note.end - note.start, midi_dto.ticks_per_beat)),
                    musecoco_abbreviations_reversed["velocity"]: str(note.velocity),
                    musecoco_abbreviations_reversed["instrument"]: str(instrument.name)
                }
            )

    return musecoco_line

