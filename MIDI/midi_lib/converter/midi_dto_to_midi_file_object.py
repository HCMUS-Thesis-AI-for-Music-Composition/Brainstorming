from miditoolkit import MidiFile, TempoChange, KeySignature, TimeSignature, Instrument, Note, Marker
from dto.Midi import MidiDTO

import const.midi as mc
import midi_utils as mu

import dto_utils as du

def midi_dto_to_midi_file_object_converter(midi_dto: MidiDTO) -> MidiFile:
    midi_dto = du.normalize_midi_dto(midi_dto)
    
    midi_file_object = MidiFile()
    
    midi_file_object.ticks_per_beat = midi_dto.ticks_per_beat
    midi_file_object.max_tick = midi_dto.max_tick
    midi_file_object.lyrics = midi_dto.lyrics


    for tempo_change in midi_dto.tempo_changes:
        midi_file_object.tempo_changes.append(
            TempoChange(
                time=tempo_change.time,
                tempo=tempo_change.tempo
            )
        )

    for key_signature_change in midi_dto.key_signature_changes:
        key_name = key_signature_change.key_name
        
        root_note, scale = key_name.split(" ")

        scale = scale.lower().strip()
        
        # m = minor, empty = major and other scales
        if mc.ScaleName.MINOR.lower() in scale:
            scale = "m"

            if f"{root_note}{scale}" not in mc.miditoolkit_supported_keys[mc.ScaleName.MINOR]:
                root_note = mu.equivalent_note_name(root_note)
            else:
                pass
        else:
            scale = ""
            
            if f"{root_note}{scale}" not in mc.miditoolkit_supported_keys[mc.ScaleName.MAJOR]:
                root_note = mu.equivalent_note_name(root_note)
            else:
                pass

        key_name = f"{root_note}{scale}"

        midi_file_object.key_signature_changes.append(
            KeySignature(
                time=key_signature_change.time,
                key_name=key_name
            )            
        )

    for time_signature_change in midi_dto.time_signature_changes:
        midi_file_object.time_signature_changes.append(
            TimeSignature(
                time=time_signature_change.time,
                numerator=time_signature_change.time_signature.numerator,
                denominator=time_signature_change.time_signature.denominator
            )
        )

    for instrument_info in midi_dto.instruments:
        instrument = Instrument(
            name=instrument_info.name, 
            program=instrument_info.program,
            notes=[]
        )

        for note_info in instrument_info.notes:
            note = Note(
                start=note_info.start,
                end=note_info.end,
                pitch=note_info.pitch,
                velocity=note_info.velocity
            )

            instrument.notes.append(note)

        midi_file_object.instruments.append(instrument)

    for marker_info in midi_dto.markers:
        midi_file_object.markers.append(
            Marker(
                time=marker_info.time,
                text=marker_info.text
            )
        )

    return midi_file_object