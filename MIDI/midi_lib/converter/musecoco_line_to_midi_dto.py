from dto.Midi import MidiDTO
from dto.Instrument import InstrumentDTO
from dto.Note import NoteDTO
from dto.TimeSignatureChange import TimeSignatureChangeDTO
from dto.TimeSignature import TimeSignatureDTO
from midi_utils import beat_to_tick
import const.musecoco_const as musecoco_const

def musecoco_line_to_midi_dto_converter(musecoco_line: list) -> MidiDTO:
    midi_dto = MidiDTO()

    midi_dto.ticks_per_beat = 960
    midi_dto.max_tick = 30721
    midi_dto.time_signature_changes = []

    current_position = 0
    current_duration = 0
    current_pitch = 0
    current_velocity = 0
    current_instrument = 0

    midi_dto.instruments = []

    for pair in musecoco_line:
        key = list(pair.keys())[0]
        value = pair[key]
        
        match key:
            case musecoco_const.str_abbr_time_signature:
                midi_dto.time_signature_changes.append(
                    TimeSignatureChangeDTO(
                        time = current_position,
                        time_signature = musecoco_const.musecoco_time_signature_mapper[
                            int(value)
                        ]
                    )
                )
            case musecoco_const.str_abbr_position:
                current_position = int(value)
            case musecoco_const.str_abbr_pitch:
                current_pitch = int(value)
            case musecoco_const.str_abbr_duration:
                current_duration = int(value)
            case musecoco_const.str_abbr_velocity:
                current_velocity = int(value)
            case musecoco_const.str_abbr_instrument:
                current_instrument = int(value)

        if key == musecoco_const.str_abbr_velocity:
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