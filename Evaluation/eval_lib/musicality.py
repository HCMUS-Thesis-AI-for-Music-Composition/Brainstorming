from MIDI.midi_lib.converter.midi_file_object_to_midi_dto import midi_file_object_to_midi_dto_converter
from MIDI.midi_lib.midi_file_utils import read_midi_file
from MIDI.midi_lib.dto.Note import NoteDTO
from MIDI.midi_lib.dto.Midi import MidiDTO


from collections import Counter

def pitch_count(notes: list[NoteDTO]) -> dict:
    pitches = [note.pitch for note in notes]
    result = dict(Counter(pitches))