class TempoChangeDTO:
    """
        Attributes:
            time: int
                The time in ticks when the tempo change occurs.
            tempo: float
                The tempo at the time of the tempo change.
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                tempo: float
        """
        self.time: int = int(0)
        self.tempo: float = float(0)

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
                "tempo": type(self.tempo)
            }
            
            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")