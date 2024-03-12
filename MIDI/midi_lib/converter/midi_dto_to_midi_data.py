from miditoolkit import MidiFile, TempoChange, KeySignature, TimeSignature, Instrument, Note, Marker
from dto.Midi import MidiDTO

def midi_dto_to_midi_data_converter(midi_dto: MidiDTO) -> MidiFile:
    midi_data = MidiFile()
    
    midi_data.ticks_per_beat = midi_dto.ticks_per_beat
    midi_data.max_tick = midi_dto.max_tick
    midi_data.lyrics = midi_dto.lyrics


    for tempo_change in midi_dto.tempo_changes:
        midi_data.tempo_changes.append(
            TempoChange(
                time=tempo_change.time,
                tempo=tempo_change.tempo
            )
        )

    for key_signature_change in midi_dto.key_signature_changes:
        midi_data.key_signature_changes.append(
            KeySignature(
                time=key_signature_change.time,
                key_name=key_signature_change.key_name
            )            
        )

    for time_signature_change in midi_dto.time_signature_changes:
        midi_data.time_signature_changes.append(
            TimeSignature(
                time=time_signature_change.time,
                numerator=time_signature_change.numerator,
                denominator=time_signature_change.denominator
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

        midi_data.instruments.append(instrument)

    for marker_info in midi_dto.markers:
        midi_data.markers.append(
            Marker(
                time=marker_info.time,
                text=marker_info.text
            )
        )

    return midi_data