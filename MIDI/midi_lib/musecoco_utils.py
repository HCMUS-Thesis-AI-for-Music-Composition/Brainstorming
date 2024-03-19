from dto.TimeSignature import TimeSignatureDTO

def generate_time_signature_dict(
    max_ts_denominator_power, 
    max_notes_per_bar
) -> dict:
    # The logic below is from
    # musecoco/muzic/musecoco/2-attribute2music_model/midiprocessor/vocab_manager.py
    idx = 0
    ts_dict = dict()
    for i in range(0, max_ts_denominator_power + 1):  # 1 ~ 64
        for j in range(1, ((2 ** i) * max_notes_per_bar) + 1):
            ts_dict[idx] = TimeSignatureDTO(
                numerator=j, 
                denominator=2 ** i
            )
            
            idx += 1
            
    return ts_dict