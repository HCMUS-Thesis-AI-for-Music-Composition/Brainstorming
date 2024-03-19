from miditoolkit import MidiFile, TempoChange, KeySignature, TimeSignature, Instrument, Note, Marker
from dto.Midi import MidiDTO

def midi_dto_to_midi_file_object_converter(midi_dto: MidiDTO) -> MidiFile:
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
        midi_file_object.key_signature_changes.append(
            KeySignature(
                time=key_signature_change.time,
                key_name=key_signature_change.key
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