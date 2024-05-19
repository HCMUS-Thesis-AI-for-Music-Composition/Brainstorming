class KeySignatureChangeDTO:
    """
        Attributes:
            time: int
            key_name: str
                Example: Db Major, A minor, etc.
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                key_name: str
                    Example: Db Major, A minor, etc.
        """
        self.time: int = int(0)
        self.key_name: str = ""

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
                "key_name": type(self.key_name)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")