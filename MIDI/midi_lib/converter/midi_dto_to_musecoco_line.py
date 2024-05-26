from dto.Midi import MidiDTO
from musecoco_original_libs.vocab_manager import VocabManager

from midi_utils import current_tempo_from_midi_dto_tempo_changes
from converter.note_position import tick_to_position_converter
import midi_lib.const.musecoco_const as musecoco_const

def midi_dto_to_musecoco_line_converter(
    midi_dto: MidiDTO, 
    vocab_manager: VocabManager = VocabManager()
) -> list:
    print(f"DEBUG: midi_dto: {midi_dto.ticks_per_beat}")
    musecoco_line = []

    time_sig = (
        midi_dto.time_signature_changes[0].time_signature.numerator, 
        midi_dto.time_signature_changes[0].time_signature.denominator
    )

    if time_sig == (12, 4):
        time_sig = (12, 8)
    elif time_sig == (9, 4):
        time_sig = (9, 8)
    else:
        pass

    musecoco_line.append(
        (
            musecoco_const.str_abbr_time_signature, 
            vocab_manager.convert_ts_to_id(
                time_sig
            )
        )
    )

    current_instrument_program = 0
    current_instrument_name = ""
    current_position = -1
    current_tempo = 0

    should_note_be_put_in_the_same_place_with_previous_note = False

    for instrument in midi_dto.instruments:
        for note in instrument.notes:
            should_note_be_put_in_the_same_place_with_previous_note = (
                (
                    current_position == tick_to_position_converter(
                        tick=note.start, 
                        tick_per_beat=midi_dto.ticks_per_beat
                    )
                ) 
                and (current_instrument_program == instrument.program)
                and (current_instrument_name == instrument.name)
                # and (current_tempo == midi_dto.tempo)
            )            

            if not should_note_be_put_in_the_same_place_with_previous_note:
                musecoco_line.append(
                    (
                        musecoco_const.str_abbr_position, tick_to_position_converter(
                            tick=note.start,
                            tick_per_beat=midi_dto.ticks_per_beat
                        )
                    )
                )
                musecoco_line.append(
                    (
                        musecoco_const.str_abbr_tempo, vocab_manager.convert_tempo_to_id(
                            current_tempo_from_midi_dto_tempo_changes(
                                midi_dto_tempo_changes=midi_dto.tempo_changes, 
                                note_position=note.start
                            )
                        )
                    )
                )
                musecoco_line.append(
                    (musecoco_const.str_abbr_instrument, instrument.program)
                )
            else:
                pass
                
            musecoco_line.append((musecoco_const.str_abbr_pitch, note.pitch))
            musecoco_line.append(
                (
                    musecoco_const.str_abbr_duration, vocab_manager.convert_dur_to_id(
                        tick_to_position_converter(
                            tick=note.end - note.start,
                            tick_per_beat=midi_dto.ticks_per_beat
                        )
                    )
                )
            )
            musecoco_line.append(
                (
                    musecoco_const.str_abbr_velocity, 
                    vocab_manager.convert_vel_to_id(note.velocity)
                )
            )

    return musecoco_line