class NoteDTO:
    start: int = 0
    end: int = 0
    pitch: int = 0
    velocity: int = 0

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                start: int
                end: int
                pitch: int
                velocity: int
        """
        
        for key, value in kwargs.items():
            type_of_keys = {
                "start": type(self.start),
                "end": type(self.end),
                "pitch": type(self.pitch),
                "velocity": type(self.velocity)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")

class InstrumentDTO:            
    program: int = 0
    name: str = ""
    notes: list[NoteDTO] = []

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                program: int
                name: str
                notes: list[NoteDTO]
        """

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

class MarkerDTO:
    time: int = 0
    text: str = ""

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                text: str
        """

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
            
class TempoChangeDTO:
    time: int = 0
    bpm: int = 0

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                bpm: int
        """

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
                "bpm": type(self.bpm)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")

class KeySignatureChangeDTO:
    time: int = 0
    key: int = 0
    scale: int = 0

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                key: int
                scale: int
        """

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

class TimeSignatureChangeDTO:
    time: int = 0
    numerator: int = 0
    denominator: int = 0

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                time: int
                numerator: int
                denominator: int
        """

        for key, value in kwargs.items():
            type_of_keys = {
                "time": type(self.time),
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

class MidiDTO:
    ticks_per_beat: int = 960
    max_tick: int = 30721
    lyrics: str = "" 
    tempo_changes: list[TempoChangeDTO] = []
    key_signature_changes: list[KeySignatureChangeDTO] = []
    time_signature_changes: list[TimeSignatureChangeDTO] = []
    instruments: list[InstrumentDTO] = []
    markers: list[MarkerDTO] = []

    def __init__(self, **kwargs):
        """
            kwargs accepts:
                ticks_per_beat: int
                max_tick: int
                lyrics: str
                tempo_changes: list[TempoChangeDTO]
                key_signature_changes: list[KeySignatureChangeDTO]
                time_signature_changes: list[TimeSignatureChangeDTO]
                instruments: list[InstrumentDTO]
                markers: list[MarkerDTO]
        """

        for key, value in kwargs.items():
            type_of_keys = {
                "ticks_per_beat": type(self.ticks_per_beat),
                "max_tick": type(self.max_tick),
                "lyrics": type(self.lyrics),
                "tempo_changes": type(self.tempo_changes),
                "key_signature_changes": type(self.key_signature_changes),
                "time_signature_changes": type(self.time_signature_changes),
                "instruments": type(self.instruments),
                "markers": type(self.markers)
            }

            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")