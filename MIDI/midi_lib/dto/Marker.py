class MarkerDTO:

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                text: str
        """
        self.time: int = int(0)
        self.text: str = str("")

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
                "text": type(self.text)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")