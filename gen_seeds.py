# -*- coding: utf-8 -*-
import os, sys

# 构造8个种子文件，长度为目标程序必须读入的最小字节数
# 每个字节分别为 0x00, 0x22, 0x44, 0x66, 0x88, 0xaa, 0xcc, 0xee

def gen_seeds(testcase_dir):
    testcase_dir = testcase_dir.strip("/")
    base = testcase_dir.split("/")[-1]
    INPUT_SIZE = base.split("_")[0].strip()
    if not INPUT_SIZE.startswith("IS"):
        print("testcase dir name format error!")
        exit(0)
    INPUT_SIZE = int(INPUT_SIZE[2:])
    seed_dir = os.path.join(testcase_dir, "seeds")
    os.system("rm -r %s" %(seed_dir))
    os.makedirs(seed_dir)

    e = 0x00
    for i in range(0, 8):
        with open(os.path.join(seed_dir, "seed%d"%(i)), "wb") as fp:
            arr = []
            for j in range(0, INPUT_SIZE):
                arr.append(e)
            fp.write(bytearray(arr))
        e = e + 0x22


if __name__ == "__main__":
    gen_seeds(sys.argv[1])
