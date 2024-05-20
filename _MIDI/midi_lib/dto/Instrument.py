from dto.Note import NoteDTO

class InstrumentDTO:            
    """
        Attributes:
            program: int
            name: str
            notes: list[NoteDTO]
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                program: int
                name: str
                notes: list[NoteDTO]
        """
        self.program: int = int(0)
        self.name: str = str("")
        self.notes: list[NoteDTO] = list[NoteDTO]([])

        for key, value in kwargs.items():
            type_of_keys = {
                "program": type(self.program),
                "name": type(self.name),
                "notes": type(self.notes)
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