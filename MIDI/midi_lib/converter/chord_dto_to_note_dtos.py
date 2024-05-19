from dto.Note import NoteDTO
from dto.Chord import ChordDTO
from dto.KeyFormula import KeyFormulaDTO

import const.hooktheory_const as htc
import midi_utils as mu

import const.midi as mc

def chord_dto_to_note_dtos_converter(
    chord_dto: ChordDTO
) -> list[NoteDTO]:
    """
        Convert a ChordDTO to a list of NoteDTOs
    """
    chord_voice_accidentals = {
        chord_voice : None
        for chord_voice in range(1, mc.default_max_chord_voice_degree + 1)
    }

    # ROOT
    chord_root_note_scale_degree = chord_dto.root # scale degree
    
    # KEY SIGNATURE
    key_tonic_note_number = chord_dto.key_signature.tonic_midi_note_number % mc.n_semitones_per_octave
    scale_formula = mc.scale_formulas[chord_dto.key_signature.scale_name]
    
    # BORROWED
    borrowed = chord_dto.borrowed
    
    if borrowed is not None:
        if type(borrowed) == list:
            n_intervals = len(borrowed)
            if n_intervals == 0:
                pass
            else:
                if n_intervals not in [
                        len(formula)
                        for scale, formula in mc.scale_formulas.items()
                ]:
                    print(
                        f"chord_dto_to_note_dtos_converter: Warning: unusual scale_length = {len(borrowed)} with {borrowed} scale"
                    )
                else:
                    pass
                
                key_tonic_note_number = key_tonic_note_number + borrowed[0]

                n_note_in_borrowed_scale = len(borrowed)

                scale_formula = [
                    (
                        borrowed[(i + 1) % n_note_in_borrowed_scale]
                        + mc.n_semitones_per_octave
                        - borrowed[i]
                    ) % mc.n_semitones_per_octave
                    for i in range(0, n_note_in_borrowed_scale)
                ]
        elif borrowed in mc.scale_formulas.keys():
            scale_formula = mc.scale_formulas[borrowed]
        elif borrowed == "super:2":
            key_tonic_note_number = key_tonic_note_number + 1
            scale_formula = mc.scale_formulas[mc.ScaleName.LOCRIAN]
        elif borrowed == "":
            pass
        else:
            raise RuntimeError(
                f"Warning: not implemented scale {borrowed} (borrowed scale)"
            )
    else:
        pass

    # APPLIED (secondary chords)
    applied = chord_dto.applied
    if applied is not None:
        if applied == 0:
            pass
        else:
            old_chord_root_note_note_number = mu.scale_degree_to_midi_note_number(
                scale_degree_str=str(chord_root_note_scale_degree),
                key_formula=KeyFormulaDTO(
                    tonic_midi_note_number=key_tonic_note_number,
                    scale_formula=scale_formula
                ),
                octave=htc.chord_default_octave
            )

            # Change to the secondary key signature
            key_tonic_note_number = old_chord_root_note_note_number % mc.n_semitones_per_octave
            scale_formula = mc.scale_formulas[mc.ScaleName.MAJOR]

            chord_root_note_scale_degree = applied
    else:
        pass

    # TYPE
    n_note_based_on_type = (chord_dto.type - 1) // 2 + 1
    for note_idx in range(0, n_note_based_on_type):
        chord_voice_accidentals[
            int(2 * note_idx + 1)
        ] = mc.AccidentalIntValue.NATURAL

    # ADDS
    for add_note in chord_dto.adds:
        chord_voice_accidentals[
            int(add_note)
        ] = mc.AccidentalIntValue.NATURAL

    # OMITS
    for omit_note in chord_dto.omits:
        chord_voice_accidentals[int(omit_note)] = None

    # SUSPENSIONS
    for sus_note in chord_dto.suspensions:
        if sus_note in [2, 4, "2", "4"]:
            chord_voice_accidentals[int(sus_note)] = mc.AccidentalIntValue.NATURAL
            chord_voice_accidentals[3] = None
        else:
            raise ValueError(f"Unsupported sus note: {sus_note}")
        
    # ALTERATIONS
    for alt_note in chord_dto.alterations:
        letter_idx = 0
        n_sharp = 0
        n_flat = 0

        for letter_idx in range(0, len(alt_note)):
            if alt_note[letter_idx] == "b":
                n_flat += 1
            elif alt_note[letter_idx] == "#":
                n_sharp += 1
            else:
                break
        
        scale_degree = int(alt_note[letter_idx:])

        chord_voice_accidentals[int(scale_degree)] = (
            n_sharp * mc.AccidentalIntValue.SHARP
            + n_flat * mc.AccidentalIntValue.FLAT
        )

    # ALTERNATE
    alternate = chord_dto.alternate
    if alternate is not None and alternate != "":
        print(f"Ignored alternate value: {alternate}")
    else:
        pass

    # INVERSION
    for i_inversion in range(1, chord_dto.inversion + 1):
        voice = 2 * i_inversion - 1

        if chord_voice_accidentals[voice] is not None:
            chord_voice_accidentals[voice] += mc.n_semitones_per_octave
        else:
            pass

    # PEDAL
    # Check this link: https://www.hooktheory.com/blog/pedal-harmony-hooktheory-i-excerpt/

    note_dtos = []

    lowest_voice_note_number = None
    
    for chord_voice, accidental in chord_voice_accidentals.items():
        if accidental is not None:
            chord_voice_scale_degree = (
                chord_root_note_scale_degree 
                + chord_voice 
                - 1
            )
            
            octave = htc.chord_default_octave

            voice_scale_degree_note_number = mu.scale_degree_to_midi_note_number(
                scale_degree_str=str(chord_voice_scale_degree),
                key_formula=KeyFormulaDTO(
                    tonic_midi_note_number=key_tonic_note_number,
                    scale_formula=scale_formula
                ),
                octave=octave
            )

            chord_voice_note_number = voice_scale_degree_note_number + accidental

            if lowest_voice_note_number is not None:
                lowest_voice_note_number = min(
                    lowest_voice_note_number,
                    chord_voice_note_number
                )
            else:
                lowest_voice_note_number = chord_voice_note_number
            
            note_dtos.append(
                NoteDTO(
                    pitch=chord_voice_note_number,
                    start=chord_dto.start,
                    end=chord_dto.end,
                    velocity=chord_dto.velocity
                )
            )
        else:
            pass
        
    if lowest_voice_note_number is not None:
        note_dtos.append(
            NoteDTO(
                pitch=(
                    lowest_voice_note_number
                    - htc.n_octave_lower_for_bass_notes * mc.n_semitones_per_octave
                ),
                start=chord_dto.start,
                end=chord_dto.end,
                velocity=chord_dto.velocity
            )
        )
    else:
        pass

    return note_dtos