from dto.Midi import MidiDTO

import const_lib.midi as mc

def normalize_midi_dto_pitch(
    midi_dto: MidiDTO
) -> MidiDTO:
    """
        Normalizes the pitch of the notes in the MidiDTO object.
        If the highest pitch is bigger than 127, the pitch is reduced to the range [0, 127].
        If the lowest pitch is smaller than 0, the pitch is increased to the range [0, 127].
        
        midi_dto: MidiDTO
            The MidiDTO object to normalize.
    """
    min_pitch = 127
    max_pitch = 0

    for instrument in midi_dto.instruments:
        for note in instrument.notes:
            if note.pitch < min_pitch:
                min_pitch = note.pitch
            if note.pitch > max_pitch:
                max_pitch = note.pitch

    pitch_delta = 0

    if min_pitch < 0:
        while min_pitch < 0:
            min_pitch += mc.n_semitones_per_octave
            pitch_delta += mc.n_semitones_per_octave
    elif max_pitch > 127:
        while max_pitch > 127:
            max_pitch -= mc.n_semitones_per_octave
            pitch_delta -= mc.n_semitones_per_octave
    else:
        pitch_delta = 0

    if pitch_delta == 0:
        pass
    else:
        for instrument in midi_dto.instruments:
            for note in instrument.notes:
                note.pitch += pitch_delta

    return midi_dto

def normalize_midi_dto_tempo(
    midi_dto: MidiDTO
) -> MidiDTO:
    """
        Normalizing tempo changes in the MidiDTO object.
        If the tempo is smaller than 0, the tempo is set to the default tempo in the const.midi module (120 BPM).
        
        midi_dto: MidiDTO
            The MidiDTO object to normalize.
    """
    for tempo_change in midi_dto.tempo_changes:
        if tempo_change.tempo <= 0:
            tempo_change.tempo = mc.default_tempo
        else:
            pass

    return midi_dto

def normalize_midi_dto(
    midi_dto: MidiDTO
) -> MidiDTO:
    """
        Normalizes the MidiDTO object.
        
        midi_dto: MidiDTO
            The MidiDTO object to normalize.
    """
    midi_dto = normalize_midi_dto_pitch(midi_dto)
    midi_dto = normalize_midi_dto_tempo(midi_dto)

    return midi_dto