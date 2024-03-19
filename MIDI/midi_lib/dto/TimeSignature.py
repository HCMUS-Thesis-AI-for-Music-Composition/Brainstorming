class TimeSignatureDTO:
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                numerator: int
                denominator: int
        """
        self.numerator = int(0)
        self.denominator = int(0)

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