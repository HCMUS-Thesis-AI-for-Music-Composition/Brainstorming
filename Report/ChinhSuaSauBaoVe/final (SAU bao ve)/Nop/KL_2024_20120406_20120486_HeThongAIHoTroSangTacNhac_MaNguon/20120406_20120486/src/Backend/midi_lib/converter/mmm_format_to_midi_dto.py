from const.midi import default_ticks_per_beat, midi_program_to_instrument_name_mapper, default_velocity, default_drums_instrument
import const.mmm_format_const as mmm_const

from dto.Instrument import InstrumentDTO
from dto.Note import NoteDTO
from dto.Midi import MidiDTO

from converter.note_position import position_to_tick_converter

from copy import deepcopy

def mmm_format_to_midi_dto_converter(
    mmm_format: list[tuple],
    tick_per_beat: int = default_ticks_per_beat,
) -> MidiDTO:
    midi_dto = MidiDTO()

    midi_dto.ticks_per_beat = tick_per_beat
    midi_dto.max_tick = 0
    midi_dto.lyrics = ""
    midi_dto.tempo_changes = []
    midi_dto.key_signature_changes = []
    midi_dto.time_signature_changes = []
    midi_dto.instruments = []
    midi_dto.markers = []

    current_time_delta = 0
    current_instrument = None
    pending_note_on = dict() # note : on_time_delta

    max_time_delta = -1
    first_peace_start = True
    for key, value in mmm_format:
        if key in [
            mmm_const.abbr_mmm_piece_start,
            mmm_const.abbr_mmm_genre,
            mmm_const.abbr_mmm_track_start,
            mmm_const.abbr_mmm_density,
            mmm_const.abbr_mmm_bar_start,
            mmm_const.abbr_mmm_bar_end
        ]:
            continue
        elif key == mmm_const.abbr_mmm_track_end:
            midi_dto.instruments.append(current_instrument)
            current_instrument = None
        elif key == mmm_const.abbr_mmm_time_delta:
            current_time_delta += float(value)
            max_time_delta = max(max_time_delta, current_time_delta)
        elif key == mmm_const.abbr_mmm_instrument:
            if type(value) == str:
                if value == "DRUMS":
                    current_instrument = InstrumentDTO(
                        program=default_drums_instrument,
                        name=midi_program_to_instrument_name_mapper[default_drums_instrument]
                    )
            elif current_instrument == None:
                current_instrument = InstrumentDTO(
                    program=int(value),
                    name=midi_program_to_instrument_name_mapper[int(value)],
                )

                current_time_delta = 0
            else:
                if int(value) == current_instrument.program:
                    continue
                else:
                    midi_dto.instruments.append(deepcopy(current_instrument))
                    current_instrument = InstrumentDTO(
                        program=int(value),
                        name=midi_program_to_instrument_name_mapper[int(value)],
                    )

                    current_time_delta = 0

                    # DEBUG
                    if len(pending_note_on) > 0:
                        print("Warning: There are pending note on")
                        print(pending_note_on)
                        print(current_instrument.program, current_time_delta)
                    # DEBUG

                    pending_note_on.clear()
        elif key == mmm_const.abbr_mmm_note_on:
            note_on = int(value)
            pending_note_on[note_on] = current_time_delta
        elif key == mmm_const.abbr_mmm_note_off:
            note_off = int(value)
            if note_off in pending_note_on:
                note_start_time = pending_note_on.pop(note_off)
                note_start_time = position_to_tick_converter(
                    note_start_time, 
                    midi_dto.ticks_per_beat,
                    position_resolution=1
                )

                note_end_time = position_to_tick_converter(
                    current_time_delta, 
                    midi_dto.ticks_per_beat,
                    position_resolution=1
                )

                current_instrument.notes.append(
                    NoteDTO(
                        start=note_start_time,
                        end=note_end_time,
                        pitch=note_off,
                        velocity=default_velocity
                    )
                )
            else:
                print(f"Note off {note_off} has no corresponding note on")
        else:
            raise ValueError(f'Unknown event: {key} with value: "{value}"')

    midi_dto.max_tick = position_to_tick_converter(
        max_time_delta, 
        midi_dto.ticks_per_beat,
        position_resolution=1
    )

    return midi_dto