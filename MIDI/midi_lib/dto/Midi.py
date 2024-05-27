from dto.TempoChange import TempoChangeDTO
from dto.KeySignatureChange import KeySignatureChangeDTO
from dto.TimeSignatureChange import TimeSignatureChangeDTO
from dto.Instrument import InstrumentDTO
from dto.Marker import MarkerDTO

# from midi_lib.const.midi import default_ticks_per_beat, default_max_tick
from const.midi import default_ticks_per_beat, default_max_tick

class MidiDTO:
    """
        Attributes:
            ticks_per_beat: int
            max_tick: int
            lyrics: str
            tempo_changes: list[TempoChangeDTO]
            key_signature_changes: list[KeySignatureChangeDTO]
            time_signature_changes: list[TimeSignatureChangeDTO]
            instruments: list[InstrumentDTO]
            markers: list[MarkerDTO]
    """
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

        self.ticks_per_beat: int = int(default_ticks_per_beat)
        self.max_tick: int = int(default_max_tick)
        self.lyrics: str = str("") 
        self.tempo_changes: list[TempoChangeDTO] = list[TempoChangeDTO]([])
        self.key_signature_changes: list[KeySignatureChangeDTO] = list[KeySignatureChangeDTO]([])
        self.time_signature_changes: list[TimeSignatureChangeDTO] = list[TimeSignatureChangeDTO]([])
        self.instruments: list[InstrumentDTO] = list[InstrumentDTO]([])
        self.markers: list[MarkerDTO] = list[MarkerDTO]([])
        
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

            # Các thuộc tính dạng list chỉ được kiểm tra giá trị truyền vào có phải là list hay không
            # Không kiểm tra các PHẦN TỬ trong list có thỏa mãn kiểu dữ liệu hay không
            if key in type_of_keys:
                if not type(value) == type_of_keys[key]:
                    raise ValueError(f"Expected {type_of_keys[key]} for {key}, got {type(value)}")
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")