def str2objects(spec):
    spec = spec.lower()
    values= {
        'dict': {},
        'list': [],
        'str' : ''
    }
    if not spec:
        return []
    if spec in values:
        return [values[spec]]
    else:
        items = spec.split(" ")
    def build_rest(lst, index):
        if index == len(lst):
            return ""
        tail = build_rest(lst, index + 1)
        if tail == "":
            return lst[index]
        return lst[index] + " " + tail

    rest = build_rest(items, 1)

    return [values[items[0]]] + str2objects(rest)


#test
print(str2objects("dict list str dict"))
#[{}, [], '', {}]
print(str2objects('dict'))