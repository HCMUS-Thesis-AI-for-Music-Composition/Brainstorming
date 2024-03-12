class NoteDTO:
    start: int = int(0)
    end: int = int(0)
    pitch: int = int(0)
    velocity: int = int(0)

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                start: int
                end: int
                pitch: int
                velocity: int
        """
        
        for key, value in kwargs.items():
            type_of_keys = {
                "start": type(self.start),
                "end": type(self.end),
                "pitch": type(self.pitch),
                "velocity": type(self.velocity)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")