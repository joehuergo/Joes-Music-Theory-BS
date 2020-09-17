###########################
# --- MISC. FUNCTIONS --- #
###########################


def common_data(list1, list2):
    result = False
    # traverse in the 1st list
    for x in list1:
        # traverse in the 2nd list
        for y in list2:
            # if one common
            if x == y:
                result = True
                return result
    return result


def flatten_list(inp):
    output = []
    for i in inp:
        if type(i) == list:
            output.extend(flatten_list(i))
        else:
            output.append(i)
    return output


def prune_copies(inp):
    list_len = len(inp)
    i = 0
    while i < list_len:
        j = i + 1
        while j < list_len:
            if inp[i] == inp[j]:
                inp.reverse()
                inp.remove(inp[j])
                inp.reverse()
                list_len -= 1
                j -= 1
            j += 1
        i += 1
    return inp


def depth_count(x):
    return int(isinstance(x, list)) and len(x) and 1 + max(map(depth_count, x))


def iclass(interval):
    x = interval % 12
    if x > 6:
        x = abs(12 - x)
    return x


def lcm(x, y):
    # choose the greater number
    if x > y:
        greater = x
    else:
        greater = y
    while True:
        if (greater % x == 0) and (greater % y == 0):
            lc = greater
            break
        greater += 1
    return lc
