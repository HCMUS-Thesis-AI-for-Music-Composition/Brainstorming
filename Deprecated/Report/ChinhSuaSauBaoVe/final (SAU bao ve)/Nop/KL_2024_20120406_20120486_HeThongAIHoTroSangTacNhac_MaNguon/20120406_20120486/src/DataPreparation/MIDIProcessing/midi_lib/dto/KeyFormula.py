class KeyFormulaDTO:
    """
        Attributes:
            tonic_midi_note_number: int
            scale_formula: list[int]
    """
    def __init__(self, **kwargs):
        """
            kwargs accepts:
                tonic_midi_note_number: int
                scale_formula: list[int]
        """
        self.tonic_midi_note_number: int = int(0)
        self.scale_formula: list[int] = list[int]([])

        for key, value in kwargs.items():
            type_of_keys = {
                "tonic_midi_note_number": type(self.tonic_midi_note_number),
                "scale_formula": type(self.scale_formula)
            }

            # Các thuộc tính dạng list chỉ được kiểm tra giá trị truyền vào có phải là list hay không
            # Không kiểm tra các PHẦN TỬ trong list có thỏa mãn kiểu dữ liệu hay không
            if key in type_of_keys:
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")