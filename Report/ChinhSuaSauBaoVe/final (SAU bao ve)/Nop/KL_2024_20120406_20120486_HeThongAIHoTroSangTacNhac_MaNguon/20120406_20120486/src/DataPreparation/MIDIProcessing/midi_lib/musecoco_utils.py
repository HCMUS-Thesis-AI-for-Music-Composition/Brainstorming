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

import random

import const_lib.musecoco_const as mcc

def remove_structure_errors(
    musecoco_line: list[tuple],
    next_acceptable_keys: dict = mcc.next_acceptable_keys,
    should_error_be_fixed_randomly: bool = False
) -> tuple[list[tuple], str]:
    printed_lines = ""

    valid_musecoco_line = []
    
    prev_key = musecoco_line[0][0]
    
    if prev_key != mcc.str_abbr_time_signature:
        str_to_print = f"remove_structure_errors: The first key must be '{mcc.str_abbr_time_signature}'"
        print(str_to_print)
        # valid_musecoco_line.append((mcc.str_abbr_time_signature, 9))

        printed_lines += str_to_print + "\n"
    else:
        pass

    valid_musecoco_line = []
    
    valid_musecoco_line.append(musecoco_line[0])
    
    for i in range(1, len(musecoco_line)):
        key, value = musecoco_line[i]
        
        if key in next_acceptable_keys[prev_key]:
            if should_error_be_fixed_randomly:
                v = musecoco_line[i][1]

            #     if v > 127:
            #         str_to_print = f"remove_structure_errors: {key} is not allowed to have a value greater than 127 ({musecoco_line[i]})"

            #         print(str_to_print)

            #         printed_lines += str_to_print + "\n"

            #         musecoco_line[i] = (key, random.randint(10, 25))

            #         str_to_print = f"-----> remove_structure_errors: ({key}, {random_alternative_value}) is added instead of ({key}, {value})"

            #         print(str_to_print)

            #         printed_lines += str_to_print + "\n"

            #         print()

            #         printed_lines += "\n"
            #     else:
            #         pass
            # else:
            #     pass
            
            if value > 127:
                # Ignore the value
                # str_to_print = f"remove_structure_errors: {key} is not allowed to have a value greater than 127 ({musecoco_line[i]})"
                # print(str_to_print)

                # printed_lines += str_to_print + "\n"
                
                # DEBUG
                valid_musecoco_line.append(musecoco_line[i])
                prev_key = key
            else:
                valid_musecoco_line.append(musecoco_line[i])
                prev_key = key
        else:
            str_to_print = f"remove_structure_errors: {key} is not allowed after {prev_key} ({musecoco_line[i - 1]} is followed by {musecoco_line[i]}): {musecoco_line[i - 1]}, {musecoco_line[i]}"

            print(str_to_print)

            printed_lines += str_to_print + "\n"

            if should_error_be_fixed_randomly:
                random_alternative_key = random.choice(next_acceptable_keys[prev_key])
                random_alternative_value = random.randint(10, 15)

                valid_musecoco_line.append(
                    (
                        random_alternative_key, 
                        random_alternative_value
                    )
                )

                str_to_print = f"-----> remove_structure_errors: ({random_alternative_key}, {random_alternative_value}) is added instead of ({key}, {value})"
                print(str_to_print)

                printed_lines += str_to_print + "\n"

                print()
                printed_lines += "\n"

                prev_key = random_alternative_key
            else:
                pass

    if len(valid_musecoco_line) == len(musecoco_line):
        str_to_print = "remove_structure_errors: NO STRUCTURE ERRORS FOUND"
        print(str_to_print)

        printed_lines += str_to_print + "\n"
    else:
        pass

    return valid_musecoco_line, printed_lines

def fill_missing_keys(
    musecoco_line: list[tuple],
    next_acceptable_keys: dict = mcc.next_acceptable_keys,
    should_error_be_fixed_randomly: bool = False
) -> tuple[list[tuple], str]:
    printed_logs = ""

    valid_musecoco_line = []
    
    prev_key = musecoco_line[0][0]
    
    valid_musecoco_line.append(musecoco_line[0])
    
    for i in range(1, len(musecoco_line)):
        key, value = musecoco_line[i]
        
        if key in next_acceptable_keys[prev_key]:
            valid_musecoco_line.append(musecoco_line[i])
            prev_key = key
        else:
            str_to_print = f"fill_missing_keys: {key} is not allowed after {prev_key} ({musecoco_line[i - 1]} is followed by {musecoco_line[i]}): {musecoco_line[i - 1]}, {musecoco_line[i]}"

            print(str_to_print)

            printed_logs += str_to_print + "\n"

            if should_error_be_fixed_randomly:
                random_alternative_key = random.choice(next_acceptable_keys[prev_key])
                random_alternative_value = random.randint(10, 15)

                valid_musecoco_line.append(
                    (
                        random_alternative_key, 
                        random_alternative_value
                    )
                )

                str_to_print = f"-----> fill_missing_keys: ({random_alternative_key}, {random_alternative_value}) is added instead of ({key}, {value})"
                print(str_to_print)

                printed_logs += str_to_print + "\n"

                print()
                printed_logs += "\n"

                prev_key = random_alternative_key
            else:
                pass

    if len(valid_musecoco_line) == len(musecoco_line):
        str_to_print = "fill_missing_keys: NO MISSING KEYS FOUND"
        print(str_to_print)

        printed_logs += str_to_print + "\n"
    else:
        pass

    return valid_musecoco_line, printed_logs