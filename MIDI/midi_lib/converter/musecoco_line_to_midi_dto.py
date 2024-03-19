from dto.Midi import MidiDTO

from musecoco_original_libs.vocab_manager import VocabManager
import musecoco_original_libs.midiprocessor.enc_remigen2_utils as enc_remigen2_utils
from converter.midi_file_object_to_midi_dto import midi_file_object_to_midi_dto_converter

def musecoco_line_to_midi_dto_converter(
    musecoco_line: list,
    vocab_manager: VocabManager = VocabManager()
) -> MidiDTO:
    midi_obj = enc_remigen2_utils.generate_midi_obj_from_remigen_token_list(musecoco_line, vocab_manager)

    midi_dto = midi_file_object_to_midi_dto_converter(midi_obj)

    return midi_dto

# def musecoco_line_to_midi_dto_converter(
#     musecoco_line: list, 
#     tick_per_beat=musecoco_const.musecoco_default_ticks_per_beat
# ) -> MidiDTO:
#     midi_dto = MidiDTO()

#     midi_dto.ticks_per_beat = tick_per_beat
#     midi_dto.max_tick = default_max_tick
#     midi_dto.time_signature_changes = []

#     curr_tick_pos = -1
#     curr_tick_duration = -1
#     curr_pitch = -1
#     curr_velocity = -1
#     curr_instrument_program = -1

#     midi_dto.instruments = []

#     vm = VocabManager()

#     for pair in musecoco_line:
#         key = list(pair.keys())[0]
#         value = pair[key]
        
#         match key:
#             case musecoco_const.str_abbr_time_signature:
#                 if curr_tick_pos == -1:
#                     curr_tick_pos = 0
#                 else:
#                     pass

#                 midi_dto.time_signature_changes.append(
#                     TimeSignatureChangeDTO(
#                         time = curr_tick_pos,
#                         time_signature = musecoco_const.musecoco_time_signature_mapper[
#                             int(value)
#                         ]
#                     )
#                 )
#             case musecoco_const.str_abbr_tempo:
#                 midi_dto.tempo_changes.append(
#                     TempoChangeDTO(
#                         time = curr_tick_pos,
#                         tempo = vm.convert_id_to_tempo(float(value))
#                     )
#                 )
#             case musecoco_const.str_abbr_position:
#                 curr_tick_pos = vm.pos_to_tick_time(int(value), tick_per_beat)
#             case musecoco_const.str_abbr_pitch:
#                 curr_pitch = vm.convert_id_to_pitch(int(value))
#             case musecoco_const.str_abbr_duration:
#                 curr_tick_duration = vm.convert_id_to_dur(int(value))
#             case musecoco_const.str_abbr_velocity:
#                 curr_velocity = vm.convert_id_to_vel(int(value))
#             case musecoco_const.str_abbr_instrument:
#                 curr_instrument_program = int(value)
#                 # print(f"curr_instrument_program: {curr_instrument_program}")

#         if key == musecoco_const.str_abbr_velocity:
#             note = NoteDTO(
#                 start = curr_tick_pos,
#                 end = curr_tick_pos + curr_tick_duration,
#                 pitch = curr_pitch,
#                 velocity = curr_velocity
#             )

#             if curr_instrument_program not in [instrument.name for instrument in midi_dto.instruments]:
#                 instrument = InstrumentDTO(
#                     name = str(curr_instrument_program),
#                     program = curr_instrument_program,
#                     notes = [note]
#                 )
                
#                 midi_dto.instruments.append(instrument)
#             else:
#                 for i in range(len(midi_dto.instruments)):
#                     if midi_dto.instruments[i].name == curr_instrument_program:
#                         midi_dto.instruments[i].notes.append(note)
#                         break

#     return midi_dto