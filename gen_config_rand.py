# -*- coding: utf-8 -*-
import os, random, string

config_dir = "configs"
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

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


def gen_untainted_var_range(tainted_var_range, input_size):
    white_list = [1, 4]
    tainted_var_range_map = {}
    start_lst = []
    for one in tainted_var_range:
        start, length = one
        tainted_var_range_map[start] = length
        start_lst.append(start)
    start_lst.sort()

    p = 0 #指针
    final_result = []
    for start in start_lst:
        if (start - p) > 0:
            untainted_size = start - p
            results = gen_var_range(untainted_size, untainted_size, white_list=[1, 4], untainted=True)
            # 返回变量数最少的结果
            minor_result = None
            min_len = 100000
            for result in results:
                if len(result) < min_len:
                    minor_result = result
                    min_len = len(result)
            if minor_result:
                for i in range(0, len(minor_result)):
                    s, l = minor_result[i]
                    minor_result[i] = (s + p, l)
                final_result.extend(minor_result)
        p = start + tainted_var_range_map[start]
    untainted_size = input_size - p
    if untainted_size > 0:
        results = gen_var_range(untainted_size, untainted_size, white_list=[1, 4], untainted=True)
        minor_result = None
        min_len = 100000
        for result in results:
            if len(result) < min_len:
                minor_result = result
                min_len = len(result)
        if minor_result:
            for i in range(0, len(minor_result)):
                start, length = minor_result[i]
                minor_result[i] = (start + p, length)
            final_result.extend(minor_result)
    return final_result



def gen_var_range(input_size, tainted_size, white_list=[], untainted=False):
    num_series = break_int(tainted_size)
    results = []
    if not white_list:
        white_list = [1, 4, 8]

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

    if not untainted:
        final_results = []
        for result in results:
            result2 = gen_untainted_var_range(result, input_size)
            final_results.append((result, result2))
        # [ (tainted_var_range1, untainted_var_range1), (tainted_var_range2, untainted_var_range2), ... ]
        return final_results
    else:
        # list of tainted_var_range, e.g., [[(start_index1, len1), (start_index2, len2), ...], [(start_indexN, lenN), ,...], ...]
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
        # 跳过非污点变量, UT=untainted
        if key.find("UTVAR") >= 0:
            continue
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
    ranges = gen_var_range(input_size, tainted_size)
    for tainted_range, untainted_range in ranges:
        i = 0
        var_map = {}
        config_map = {}
        config_map["@INPUT_SIZE@"] = input_size
        config_map["@TAINTED_SIZE@"] = tainted_size
        for one in tainted_range:
            i = i + 1
            start, length = one
            _type = ""
            if length == 1:
                _type = "unsigned char"
            elif length == 2 or length == 4:
                _type = "unsigned int"
            else:
                _type = "unsigned char*"
            content = "(%s, VAR%d, %d-%d)" %(_type, i, start, start+length)
            var_map["@VAR%d@"%(i)] = content
        condition_map, extra_vars = gen_conditions(var_map)
        j = 0
        for one in untainted_range:
            j = j + 1
            start, length = one
            _type = ""
            if length == 1:
                _type = "unsigned char"
            elif length == 2 or length == 4:
                _type = "unsigned int"
            else:
                _type = "unsigned char*"
            content = "(%s, UTVAR%d, %d-%d)" %(_type, j, start, start+length)
            var_map["@UTVAR%d@"%(j)] = content
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
        os.system("mv %s %s" %(_file_name, config_dir))
    return config_maps


if __name__ == "__main__":
    config_maps_4_4 = gen_config(4, 4)
    config_maps_8_4 = gen_config(8, 4)
    config_maps_8_8 = gen_config(8, 8)
    config_maps_12_4 = gen_config(12, 4)
    config_maps_16_8 = gen_config(16, 8)
    config_maps_16_4 = gen_config(16, 4)
    config_maps_16_16 = gen_config(16,16)
