import re

from dto.TempoChange import TempoChangeDTO
from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.KeySignature import KeySignatureDTO
from dto.KeyFormula import KeyFormulaDTO

from midi_lib.const import midi as mc

def equivalent_note_name(note_name: str):
    """
        Get the equivalent note name of a note name. Example: C# -> Db, Bb -> A#

        note_name: str - note name. Example: "C", "C#", "Db", "Bb", "A#"
    """
    note_name = note_name.upper()

    midi_note_number = mc.inversed_based_midi_note_numbers[note_name]

    equiv_note_name = [
        name 
        for name in mc.based_midi_note_numbers[midi_note_number]
        if note_name != name
    ][0]

    return equiv_note_name

def scale_degree_to_midi_note_number(
    scale_degree_str: str,
    octave: int = 0,
    key_signature: KeySignatureDTO=None,
    key_formula: KeyFormulaDTO = None
):
    """
        Convert a scale degree to a MIDI note number.

        scale_degree_str: str - scale degree in string format. Examples: "1", "b2", "#3"
        key_signature: KeySignatureDTO - key signature. Use this Example: KeySignatureDTO(tonic_midi_note_number, "major"). Check const.midi.ScaleName for valid scale names.
        octave: int - octave number of the root note of the scale. octave = 0 (C4) by default.
        scale_formula: list[int] - scale formula. Example: [2, 2, 1, 2, 2, 2, 1] for major scale.
    """
    # Check if scale degree is n, bn or #n
    accidental_semitones = 0
    scale_degree = 0
    if re.match(r"^\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str)
    elif re.match(r"^b\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str[1:])
        accidental_semitones = -1
    elif re.match(r"^\#\d+$", scale_degree_str):
        scale_degree = int(scale_degree_str[1:])
        accidental_semitones = 1

    tonic_midi_note_number = None

    if key_formula is None:
        if key_signature.scale_name in mc.scale_formulas.keys():
            tonic_midi_note_number = key_signature.tonic_midi_note_number % mc.n_semitones_per_octave
            scale_formula = mc.scale_formulas[key_signature.scale_name]
        else:
            raise ValueError(f"Invalid scale name: {key_signature.scale_name}")
    else:
        tonic_midi_note_number = key_formula.tonic_midi_note_number % mc.n_semitones_per_octave
        scale_formula = key_formula.scale_formula

    # 3 times scale_formula to avoid index out of range
    scale_formula = scale_formula * 3

    base_midi_note = tonic_midi_note_number + sum(
        scale_formula[:(scale_degree - 1)]
    ) + accidental_semitones
        
    return base_midi_note + 12 * octave + mc.C4_midi_note_number

def key_signature_str_to_key_signature_dto(
    key_sig_str: str
) -> KeySignatureDTO:
    """
        Converts a key signature string to a KeySignatureDTO object.

        key_sig_str: str
            The key signature string to convert.

            Example: "C major", "F# minor", "Bb major", "Eb minor"
    """
    key_sig_str = key_sig_str.replace(" ", "")
    
    if "b" in key_sig_str or "#" in key_sig_str:
        key_sig_str = f"{key_sig_str[0:2]} {key_sig_str[2:]}"
    else:
        key_sig_str = f"{key_sig_str[0:1]} {key_sig_str[1:]}"
    
    key_str_parts = key_sig_str.split(" ")

    root_note_str = key_str_parts[0]
    scale = key_str_parts[1]

    return KeySignatureDTO(
        tonic_midi_note_number=mc.inversed_based_midi_note_numbers[root_note_str],
        scale_name=scale
    )

def current_tempo_from_midi_dto_tempo_changes(
    midi_dto_tempo_changes: list[TempoChangeDTO],
    note_position: int
):
    # Sort the tempo changes by time
    midi_dto_tempo_changes = sorted(
        midi_dto_tempo_changes, 
        key = lambda tempo_change: tempo_change.time
    )
    
    for tempo_change in midi_dto_tempo_changes:
        if note_position >= tempo_change.time:
            return tempo_change.tempo
        else:
            pass

def current_key_signature_from_midi_dto_key_signature_changes(
    midi_dto_key_signature_changes: list[KeySignatureChangeDTO], 
    note_position: int
):
    # Sort the key signature changes by time
    midi_dto_key_signature_changes = sorted(
        midi_dto_key_signature_changes, 
        key = lambda key_signature_change: key_signature_change.time
    )
    
    for key_signature_change in midi_dto_key_signature_changes:
        if note_position >= key_signature_change.time:
            return key_signature_change.key_name
        else:
            pass