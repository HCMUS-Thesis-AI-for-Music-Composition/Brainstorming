from dto.KeySignature import KeySignatureDTO

class ChordDTO:
    """
        Attributes:
            key_signature: KeySignatureDTO
            root: int - scale degree
            start: int - time in ticks
            end: int - time in ticks
            type: int
            inversion: int
            applied: int - secondary chord
            adds: list[int]
            omits: list[int]
            alterations: list[str]
            suspensions: list[int]
            pedal: Any
            alternate: str
            borrowed: Any
            velocity: int
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                key_signature: KeySignatureDTO
                root: int
                start: int - time in ticks
                end: int - time in ticks
                type: int
                inversion: int
                applied: int
                adds: list[int]
                omits: list[int]
                alterations: list[str]
                suspensions: list[int]
                pedal: Any
                alternate: str
                borrowed: Any
                velocity: int
        """
        self.key_signature: KeySignatureDTO = KeySignatureDTO()
        self.root: int = int(0)
        self.start: int = int(0)
        self.end: int = int(0)
        self.type: int = int(0)
        self.inversion: int = int(0)
        self.applied: int = int(0)
        self.adds: list[int] = list[int]([])
        self.omits: list[int] = list[int]([])
        self.alterations: list[str] = list[str]([])
        self.suspensions: list[int] = list[int]([])
        self.pedal = None
        self.alternate: str = str("")
        self.borrowed = None
        self.velocity: int = int(0)

        for key, value in kwargs.items():
            type_of_keys = {
                "key_signature": type(self.key_signature),
                "root": type(self.root),
                "start": type(self.start),
                "end": type(self.end),
                "type": type(self.type),
                "inversion": type(self.inversion),
                "applied": type(self.applied),
                "adds": type(self.adds),
                "omits": type(self.omits),
                "alterations": type(self.alterations),
                "suspensions": type(self.suspensions),
                "pedal": type(self.pedal),
                "alternate": type(self.alternate),
                "borrowed": type(self.borrowed),
                "velocity": type(self.velocity)
            }

            # Các thuộc tính dạng list chỉ được kiểm tra giá trị truyền vào có phải là list hay không
            # Không kiểm tra các PHẦN TỬ trong list có thỏa mãn kiểu dữ liệu hay không
            if key in type_of_keys:
                if key in ["borrowed", "pedal"]:
                    setattr(self, key, value)
                elif not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")