from dto.TimeSignature import TimeSignatureDTO

class TimeSignatureChangeDTO:
    """
        Attributes:
            time: int
            time_signature: TimeSignatureDTO
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                numerator: int
                denominator: int
        """
        self.time: int = int(0)
        self.time_signature = TimeSignatureDTO()

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
                "time_signature": type(self.time_signature)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")