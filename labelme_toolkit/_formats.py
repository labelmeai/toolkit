def pformat_list(list, max_seq_length=10):
    text = "["
    for i, item in enumerate(list):
        text += f"{item!r}, "
        if i == max_seq_length - 1:
            text += "...]"
            break
    else:
        if text != "[":
            text = text[:-2]
        text += "]"
    return text
