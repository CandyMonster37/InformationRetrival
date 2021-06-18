# -*- coding: utf-8 -*-
def vb_encode(doc_ids):
    byte_stream = []
    for num in doc_ids:
        bytes_split = []
        one_bytestream = ''
        while True:
            bytes_split.append((num % 128))
            if num < 128:
                break
            else:
                num = int(num / 128)
        bytes_split = bytes_split[::-1]
        for i in range(len(bytes_split)):
            if i == len(bytes_split) - 1:
                byte_stream.append(bytes([bytes_split[i] + 128]))
            else:
                byte_stream.append(bytes([bytes_split[i]]))
    return byte_stream


def vb_decode(byte_stream):
    doc_ids = []
    num = 0
    for i in range(len(byte_stream)):
        if ord(byte_stream[i]) < 128:
            num = num * 128 + ord(byte_stream[i])
        else:
            num = num * 128 + (ord(byte_stream[i]) - 128)
            doc_ids.append(num)
            num = 0
    return doc_ids


def print_vb_code(byte_stream):
    bytes_print = ''
    for i in range(len(byte_stream)):
        num = ord(byte_stream[i])
        one_bytestream = ''
        for j in range(8):
            one_bytestream += str(num % 2)
            num = int(num / 2)
        bytes_print += one_bytestream[::-1]
        bytes_print += ' '
    print(bytes_print)
