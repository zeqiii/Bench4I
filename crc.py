# -*- coding: utf-8 -*-
import os, sys, random, string

# 计算in_str的crc值，长度为length个字节
def crc(in_str, length):
    temp = 0
    l = length
    while(True):
        if l == 0:
            break
        index = length - l
        i = 0x80
        while True:
            if i == 0:
                break
            temp = temp * 2
            if((temp & 0x10000) != 0):
                temp = temp ^ 0x11021
            if type(in_str) == str:
                if((ord(in_str[index]) & i) != 0):
                    temp = temp ^ (0x10000 ^ 0x11021)
            elif type(in_str) == bytes:
                if((in_str[index] & i) != 0):
                    temp = temp ^ (0x10000 ^ 0x11021)
            i = i >> 1
        l = l - 1
    return temp

if __name__ == "__main__":
    hex_str = sys.argv[1]
    b_arr = (int(hex_str, 16)).to_bytes(1, byteorder='big')
    crc_val = crc(b_arr, 1)
    print(crc_val)
