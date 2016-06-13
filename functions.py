# -*- coding:utf-8 -*-


def get_something(code_source, start, end, i):
    """ Recover the text between 'start' and 'end' (as str),
    'start' & 'end' excluded"""
    length_start = len(start)
    length_end = len(end)
    buf_start = ""
    buf_end = ""
    text = ""
    flag = True
    while flag:
        i += 1
        buf_start += code_source[i]
        if len(buf_start) >= length_start:
            if buf_start == start:
                while flag:
                    i += 1
                    buf_end += code_source[i]
                    text += code_source[i]
                    if len(buf_end) >= length_end:
                        if buf_end == end:
                            text = text.replace(end, '')
                            flag = False
                        buf_end = buf_end[1: len(end)]
            buf_start = buf_start[1: len(start)]
    return text, i


def remove_piece_of_text(text, start, end, excepted=None):
    """remove the text between 'start' and 'end' str,
    'start' & 'end' encluded, except 'excepted' if it extist"""
    length_start = len(start)
    length_end = len(end)
    if excepted is not None:
        length_except = len(excepted)
        buf_except = ""
    buf = ""
    new_text = ""
    flag = True
    i = 0
    while i < len(text):
        buf += text[i]
        if excepted is not None and flag is False:
            buf_except += text[i]
        if flag:
            new_text += text[i]
        if len(buf) >= length_start and flag:
            if buf == start:
                new_text = new_text[0:len(new_text) - length_start]
                flag = False
            buf = buf[1:length_start]
        if(excepted is not None and
                len(buf_except) >= length_except and
                flag is False):
            if buf_except == excepted:
                new_text += str(excepted)
            buf_except = buf_except[1:length_except]
        if len(buf) >= length_end and flag is False:
            if buf == end:
                flag = True
                i -= 1
            buf = buf[1:length_end]
        i += 1
    return new_text
