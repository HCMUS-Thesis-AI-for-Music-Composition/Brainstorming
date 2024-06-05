
def musecoco_line_str_to_token_list_converter(musecoco_line_str: str):
    result = []

    token_str_list = musecoco_line_str.split(" ")

    for token_str in token_str_list:
        if '-' in token_str:
            key, value = token_str.split('-')
            result.append((str(key), int(value)))
        else:
            print(f"Ignore inappropriate token: {token_str}")

    return result