def musecoco_line_to_musecoco_line_string_converter(musecoco_line: list) -> str:
    musecoco_line_string = ""
    
    for k, v in musecoco_line:
        musecoco_line_string += f"{k}-{v} "

    # Remove the last space
    musecoco_line_string = musecoco_line_string[:-1]

    return musecoco_line_string