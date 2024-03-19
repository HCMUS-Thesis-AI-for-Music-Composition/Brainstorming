class KeySignatureChangeDTO:
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                key: int
                scale: int
        """
        self.time: int = int(0)
        self.key: int = int(0)
        self.scale: int = int(0)

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
                "key": type(self.key),
                "scale": type(self.scale)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")