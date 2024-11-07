from miditoolkit import MidiFile
import os

def read_midi_file(file_path):
    try:
        midi_data = MidiFile(file_path)
        return midi_data
    except Exception as e:
        raise RuntimeError("midi_file_utils.write_midi_file: Error on reading MIDI file:", e)

def write_midi_file(midi_data, output_file):
    try:
        # Delete old file if exists
        if os.path.exists(output_file):
            os.remove(output_file)
            
        midi_data.dump(output_file)
        print(f"MIDI file saved successfully: {output_file}")
    except Exception as e:
        raise RuntimeError("midi_file_utils.write_midi_file: Error on saving MIDI file:", e)
        # print("midi_file_utils.write_midi_file: Error on saving MIDI file:", e)