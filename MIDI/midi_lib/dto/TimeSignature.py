class TimeSignatureDTO:
    numerator = int(0)
    denominator = int(0)

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                numerator: int
                denominator: int
        """

        for key, value in kwargs.items():
            type_of_keys = {
                "numerator": type(self.numerator),
                "denominator": type(self.denominator)
            }
            
            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}") 