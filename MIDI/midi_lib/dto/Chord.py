from dto.KeySignature import KeySignatureDTO

class ChordDTO:
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                key_signature: KeySignatureDTO
                root: int
                start: float - time in ticks
                end: float - time in ticks
                type: int
                inversion: int
                applied: int
                adds: list[int]
                omits: list[int]
                alterations: list[str]
                suspensions: list[int]
                pedal: None - unknown type
                alternate: str
                borrowed: list[str]
        """
        self.key_signature: KeySignatureDTO = KeySignatureDTO()
        self.root: int = int(0)
        self.start: float = float(0)
        self.end: float = float(0)
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
                "borrowed": type(self.borrowed)
            }

            # Các thuộc tính dạng list chỉ được kiểm tra giá trị truyền vào có phải là list hay không
            # Không kiểm tra các PHẦN TỬ trong list có thỏa mãn kiểu dữ liệu hay không
            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")