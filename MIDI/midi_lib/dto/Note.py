class NoteDTO:
    """
        Attributes:
            start: int
            end: int
            pitch: int
            velocity: int
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                start: int - time in ticks
                end: int - time in ticks
                pitch: int
                velocity: int
        """
        self.start: int = int(0)
        self.end: int = int(0)
        self.pitch: int = int(0)
        self.velocity: int = int(0)
        
        for key, value in kwargs.items():
            type_of_keys = {
                "start": type(self.start),
                "end": type(self.end),
                "pitch": type(self.pitch),
                "velocity": type(self.velocity)
            }

            if key in type_of_keys:
                if type(value) != type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")