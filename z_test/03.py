def f(str):
    # s = "aaaasfd"
    l = list(str)
    l.sort(reverse=False)
    s = "".join(l)
    # print('F:' + s)
    return s


def g(str):
    # s = "53576562"
    l = list(str)
    l.sort(reverse=True)
    s = "".join(l)
    # print('G:' + s)
    return s


# f('aaaasfd')
# g('53576562')

str = input('str:')
flag = -1
# print(ord('?'))
# 63
res = ''
temp_str = ''
for c in str:
    ask = ord(c)
    if 97 <= ask <= 122 or 65 <= ask <= 90:
        if flag == -1 or flag == 0:
            temp_str += c
        if flag == 2 or flag == 1:
            res += g(temp_str)
            temp_str = c
        flag = 0
        # print('字母')
    if 48 <= ask <= 57:
        if flag == -1 or flag == 1:
            temp_str += c
        if flag == 2 or flag == 0:
            res += f(temp_str)
            temp_str = c
        flag = 1
        # print('数字')
    if ask == 63:
        if flag == 0:
            res += f(temp_str)
        elif flag == 1:
            res += g(temp_str)
        temp_str = ''
        res += '?'
        flag = 2
    # print(ord(c))
    # print(c)
    # print(temp_str)
if flag == 0:
    res += f(temp_str)
elif flag == 1:
    res += g(temp_str)
print(res)
