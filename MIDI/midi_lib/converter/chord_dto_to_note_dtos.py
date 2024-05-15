from dto.Note import NoteDTO
from dto.Chord import ChordDTO

import const.midi as mc
import const.hooktheory_const as htc

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
    
    # KEY SIGNATURE
    scale_formula = mc.scale_formulas[chord_dto.key_signature.scale_name]
    
    # BORROWED
    borrowed = chord_dto.borrowed
    if borrowed is not None:
        if type(borrowed) == list:
            if len(borrowed) not in [
                len(formula)
                for scale, formula in mc.scale_formulas
            ]:
                print(
                    f"Warning: unusual scale_length = {len(borrowed)} with {borrowed} scale"
                )
            else:
                print(
                    f"Message: borrowed {borrowed} scale"
                )
            
            borrowed_scale_formula = borrowed
        elif borrowed in mc.scale_formulas:
            scale_formula = mc.scale_formulas[borrowed]
        else:
            print(
                f"Warning: not implemented scale {borrowed} (borrowed scale)"
            )
    else:
        pass

    # ROOT
    root = chord_dto.root

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
    if alternate is not None:
        print(f"Ignored alternate value: {alternate}")
    else:
        pass

    # INVERSION
    available_voices = [
        voice
        for voice, accidental in chord_voice_accidentals.items()
        if accidental is not None
    ]

    available_voices.sort()

    for available_voice_idx in range(0, chord_dto.inversion):
        chord_voice_accidentals[
            available_voices[available_voice_idx]
        ] += mc.n_semitones_per_octave
        
            
    

    # TODO: Implement the rest of the function

    import json
    import sys
    
    for k, v in chord_dto.__dict__.items():
        print(f"{k}: {v}")

    print(json.dumps(chord_voice_accidentals, indent=4))
    
    # raise NotImplementedError

    return []