# from dto.TimeSignature import TimeSignatureDTO

# def generate_time_signature_dict(
#     max_ts_denominator_power, 
#     max_notes_per_bar
# ) -> dict:
#     # The logic below is from
#     # musecoco/muzic/musecoco/2-attribute2music_model/midiprocessor/vocab_manager.py
#     idx = 0
#     ts_dict = dict()
#     for i in range(0, max_ts_denominator_power + 1):  # 1 ~ 64
#         for j in range(1, ((2 ** i) * max_notes_per_bar) + 1):
#             ts_dict[idx] = TimeSignatureDTO(
#                 numerator=j, 
#                 denominator=2 ** i
#             )
            
#             idx += 1
            
#     return ts_dict

import const.musecoco_const as mcc

def remove_structure_errors(
    musecoco_line: list[tuple],
    next_acceptable_keys: dict = mcc.next_acceptable_keys
) -> list[tuple]:
    valid_musecoco_line = None
    
    prev_key = musecoco_line[0][0]
    
    if prev_key != mcc.str_abbr_time_signature:
        print(f"remove_structure_errors: The first key must be '{mcc.str_abbr_time_signature}'")
    else:
        valid_musecoco_line = []
        
        valid_musecoco_line.append(musecoco_line[0])
        
        for i in range(1, len(musecoco_line)):
            key, value = musecoco_line[i]
            
            if key in next_acceptable_keys[prev_key]:
                valid_musecoco_line.append(musecoco_line[i])
                prev_key = key
            else:
                print(
                    f"remove_structure_errors: {key} is not allowed after {prev_key} ({musecoco_line[i - 1]} is followed by {musecoco_line[i]})"
                )
                
    if len(valid_musecoco_line) == len(musecoco_line):
        print("remove_structure_errors: NO STRUCTURE ERRORS FOUND")
                
    return valid_musecoco_line