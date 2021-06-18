# -*- coding: utf-8 -*-
def vector_encode(a, doc_list):
    return list(i in a for i in doc_list)


def vector_decode(v, doc_list):
    ret = []
    for i in range(len(v)):
        if v[i]:
            ret.append(doc_list[i])
    return ret


def boolean_op(op, stack):
    if op == 'AND':
        vec1 = stack.pop()
        vec2 = stack.pop()
        res = list(map(lambda x, y: x and y, vec1, vec2))
        stack.append(res)
    elif op == 'OR':
        vec1 = stack.pop()
        vec2 = stack.pop()
        res = list(map(lambda x, y: x or y, vec1, vec2))
        stack.append(res)
    elif op == 'NOT':
        vec1 = stack.pop()
        res = list(map(lambda x: not x, vec1))
        stack.append(res)
    return stack
