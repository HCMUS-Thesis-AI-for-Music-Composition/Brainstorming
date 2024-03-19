from dto.Midi import MidiDTO

from midi_utils import current_tempo_from_midi_dto_tempo_changes
from converter.note_position import tick_to_position_converter
import const.musecoco_const as musecoco_const

def midi_dto_to_musecoco_line_converter(midi_dto: MidiDTO):
    musecoco_line = []
    
    current_position = -1
    current_instrument_program = 0
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
                and (current_tempo == midi_dto.tempo)
            )            

            if not should_note_be_put_in_the_same_place_with_previous_note:
                musecoco_line.append(
                    {
                        musecoco_const.str_abbr_position : tick_to_position_converter(
                            tick=note.start,
                            tick_per_beat=midi_dto.ticks_per_beat
                        )
                    }
                )
                musecoco_line.append(
                    {
                        musecoco_const.str_abbr_tempo : current_tempo_from_midi_dto_tempo_changes(
                            midi_dto_tempo_changes=midi_dto.tempo_changes, 
                            note_position=note.start
                        )
                    }
                )
                musecoco_line.append({musecoco_const.str_abbr_instrument : instrument.program})
            else:
                pass
                
            musecoco_line.append({musecoco_const.str_abbr_pitch : note.pitch})
            musecoco_line.append(
                {
                    musecoco_const.str_abbr_duration : tick_to_position_converter(
                        tick=note.end - note.start,
                        tick_per_beat=midi_dto.ticks_per_beat
                    )
                }
            )
            musecoco_line.append({musecoco_const.str_abbr_velocity : note.velocity})

    return musecoco_line