# -*- coding: utf-8 -*-
import random

def pp(res):
    content = []
    for i in range(0, len(res)):
        if res[i] > 0:
            content.append(res[i])
    return content
def break_int_internal(value, result, res, p):
    if value <= 0:
        content = pp(res)
        result.append(content)
        return
    for i in range(1, value+1):
        res[p] = i
        p = p + 1
        break_int_internal(value-i, result, res, p)
        p = p - 1
        for j in range(p+1, len(res)):
            res[j] = 0
# 分解整数，把一个整数分解为若干整数的加和
def break_int(value):
    result = []
    result2 = []
    res = [0 for _ in range(256)]
    p = 0
    break_int_internal(value, result, res, p)
    for one in result:
        one.sort()
        if one not in result2:
            result2.append(one)
    return result2


# [[(start_index1, len1), (start_index2, len2), ...], [(start_indexN, lenN), ,...], ...]
def gen_var_range(input_size, tainted_size):
    num_series = break_int(tainted_size)
    results = []
    white_list = [1, 4, 8, 16, 32, 64]

    for series in num_series:
        remained_space = input_size
        remained_length = tainted_size
        current_p = 0
        tainted_bytes = []
        ok = True
        for one in series:
            if one not in white_list:
                ok = False
                break
            random_space = remained_space - remained_length
            start = current_p + int(random.random() * random_space)
            tainted_bytes.append((start, one))
            current_p = start + one
            remained_length = remained_length - one
            remained_space = input_size - current_p
        if ok:
            results.append(tainted_bytes)

    return results


# (op1, ==, op2, range)  range=1
# (op1, <, op2, range)   range=0~op2, op1<op2
# (op1, >, op2, range)   range=op2~int_max, op1>op2
# (op1, &&, op2, op3, range) which is (op1>op2 && op1<op3)  range=op2~op3
# (op1, strncmp, op2, n, range) which is (strncmp(op1, op2, n) == 0) range=1
# (op1, memcmp, op2, n, range) which is (memcmp(op1, op2, n) == 0) range=1
def gen_conditions(var_maps):
    condition_maps = {}
    extra_vars = {}  # 存放一些常量定义
    i = 0
    j = 0
    for key in var_maps.keys():
        i = i + 1
        content = var_maps[key]
        parts = content.split("@=")[-1].strip("(").strip(")").split(",")
        _type = parts[0].strip()
        _name = parts[1].strip()
        _range = int(parts[2].strip().split("-")[1]) - int(parts[2].strip().split("-")[0])
        if _range == 1:
            rand = int(random.random() * 128)
            content1 = "(%s, %s, %s, %s)" %(_name, "==", hex(rand), hex(1))
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content1
        elif _range == 2:
            rand = int(random.random() * 0x10000)
            content1 = "(%s, %s, %s, %s)" %(_name, "==", hex(rand), hex(1))
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content1
            i = i + 1
            rand = int(random.random() * (0x10000-0x1000))
            content2 = "(%s, %s, %s, %s, %s)" %(_name, "&&", hex(rand), hex(rand+0x1000), "0x1000")
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content2
        elif _range == 4:
            rand = int(random.random() * 0x100000000)
            content1 = "(%s, %s, %s, %s)" %(_name, "==", hex(rand), hex(1))
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content1
            i = i + 1
            rand = int(random.random() * (0x100000000-0x1000))
            content2 = "(%s, %s, %s, %s, %s)" %(_name, "&&", hex(rand), hex(rand+0x1000), "0x1000")
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content2
            i = i + 1
            rand = int(random.random() * (0x100000000-0x100000))
            content3 = "(%s, %s, %s, %s, %s)" %(_name, "&&", hex(rand), hex(rand+0x100000), "0x100000")
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content3
            i = i + 1
            rand = int(random.random() * (0x100000000-0x10000000))
            content4 = "(%s, %s, %s, %s, %s)" %(_name, "&&", hex(rand), hex(rand+0x10000000), "0x10000000")
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content4
        else:
            rand_str = ''.join(random.sample(string.ascii_letters + string.digits, _range))
            content1 = "(%s, %s, %s, %d, %s)" %(_name, "strncmp", "\""+rand_str+"\"", _range, hex(1))
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content1
            i = i + 1
            j = j + 1
            rand_bytes_decl = "unsigned char rand_bytes%d[]={" %(j)
            for k in range(0, _range):
                rand_bytes_decl = rand_bytes_decl + hex(int(random.random()*128)) + ","
            rand_bytes_decl = rand_bytes_decl[:-1]
            rand_bytes_decl = rand_bytes_decl + "};"
            extra_vars["@EXTRA_VARS%d@"%(j)] = rand_bytes_decl
            content2 = "(%s, %s, %s, %d, %s)" %(_name, "memcmp", "rand_bytes%d"%(j), _range, hex(1))
            condition_maps["@CONDITION%d:%s@"%(i, key.strip('@'))] = content2

    # 增加两个同类型的污点变量之间的比较
    return condition_maps, extra_vars
    

def gen_config(input_size, tainted_size):
    config_maps = []
    results = gen_var_range(input_size, tainted_size)
    for result in results:
        i = 0
        var_map = {}
        config_map = {}
        config_map["@INPUT_SIZE@"] = input_size
        config_map["@TAINTED_SIZE@"] = tainted_size
        for one in result:
            i = i + 1
            start, length = one
            _type = ""
            if length == 1:
                _type = "unsigned char"
            elif length == 2 or length == 4:
                _type = "unsigned int"
            else:
                _type = "unsigned char*"
            content = "(%s, var%d, %d-%d)" %(_type, i, start, start+length)
            var_map["@VAR%d@"%(i)] = content
        condition_map, extra_vars = gen_conditions(var_map)
        config_map = dict(config_map, ** var_map)
        config_map = dict(config_map, ** condition_map)
        config_map = dict(config_map, ** extra_vars)
        config_map["@TAINTED_VAR_NUM@"] = i
        config_maps.append(config_map)
    # write config files
    for config_map in config_maps:
        _file_name = "IS%d_TS%d_TV%d.conf" %(config_map["@INPUT_SIZE@"], config_map["@TAINTED_SIZE@"], config_map["@TAINTED_VAR_NUM@"])
        config_map["@CONFIG_FILE@"] = _file_name
        fp = open(_file_name, "w")
        content = ""
        for key in sorted(config_map.keys()):
            line = key + "="
            line = line + str(config_map[key]) + "\n"
            content = content + line
        fp.write(content)
        fp.flush()
        fp.close()
    return config_maps


if __name__ == "__main__":
    config_maps_4_4 = gen_config(4, 4)
