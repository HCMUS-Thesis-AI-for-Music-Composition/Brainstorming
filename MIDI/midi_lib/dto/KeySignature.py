class KeySignatureDTO:
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                tonic_midi_note_number: int
                scale_name: str - check const.midi.ScaleName for valid scale names
        """
        self.tonic_midi_note_number: int = int(0)
        self.scale_name: str = ""
        
        for key, value in kwargs.items():
            type_of_keys = {
                "tonic_midi_note_number": type(self.tonic_midi_note_number),
                "scale_name": type(self.scale_name)
            }

            if key in type_of_keys:
                if type(value) != type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")