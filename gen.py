# -*- coding: utf-8 -*-
import os, sys, random, string
import numpy as np


TYPE_UNSIGNED_CHAR = "unsigned char"
TYPE_UNSIGNED_CHAR_P = "unsigned char*"
TYPE_CHAR = "char"
TYPE_CHAR_P = "char*"
TYPE_UNSIGNED_INT = "unsigned int"
TYPE_UNSIGNED_INT_P = "unsigned int*"
TYPE_BOOL = "bool"
TYPE_BOOL_P = "bool*"

FUN_READ_UNSIGNED_INT32 = "read_unsigned_int32"
FUN_READ_UNSIGNED_INT16 = "read_unsigned_int16"

testcase_dir = "testcases"

def to_intarray(hex_str):
    arr = []
    ch = ['a', 'b', 'c', 'd', 'e', 'f']
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str
    for index in range(0, len(hex_str)/2):
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
# 分解整数
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
    i = 0
    for config_map in config_maps:
        #i = i + 1
        #_file_name = "IS%d_TS%d_TV%d_%d.conf" %(config_map["@INPUT_SIZE@"], config_map["@TAINTED_SIZE@"], config_map["@TAINTED_VAR_NUM@"], i)
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


def _gen_path(conditions):
    if len(conditions.keys()) <= 1:
        result_paths = []
        for one in conditions[conditions.keys()[0]]:
            result_paths.append([one])
        return result_paths
    else:
        cond_ids = conditions.pop(conditions.keys()[0])
        paths = _gen_path(conditions)
        result_paths = []
        for one in cond_ids:
            new_paths = []
            for path in paths:
                new_path = []
                for node in path:
                    new_path.append(node)
                new_paths.append(new_path)
            for path in new_paths:
                path.append(one)
                result_paths.append(path)
        return result_paths


def gen_struct(config_map):
    conditions = {}
    for key in config_map.keys():
        if key.startswith("@CONDITION"):
            cond_id = key.split(":")[0]
            var_id = key.split(":")[1]
            if var_id not in conditions.keys():
                conditions[var_id] = [cond_id]
            else:
                conditions[var_id].append(cond_id)
    # 一个变量可能属于多个constraints，输出所有可能的组合
    paths = _gen_path(conditions)
    i = 0
    # 每一个组合将形成一个struct配置文件
    for path in paths:
        content = ""
        tmp_stack = []
        i = i + 1
        for one in path:
            current_cond = ""
            for key in config_map.keys():
                if key.startswith(one):
                    current_cond = key
                    break
            content = content + current_cond + "\n"
            tmp_stack.append(current_cond)
        content = content + "@BUG@" + "\n"
        while True:
            if not tmp_stack:
                break
            content = content + "@ELSE@-" + tmp_stack.pop() + "\n"
        content = "#@CONFIG_FILE@=%s"%(config_map["@CONFIG_FILE@"]) + "\n" + content
        struct_file = config_map["@CONFIG_FILE@"][:-5] + "_struct%d"%(i) + ".conf"
        with open(struct_file, "w") as fp:
            fp.write(content)
        # 生成testcase文件夹
        dirname = os.path.splitext(config_map["@CONFIG_FILE@"])[0] + "__" + str(i)
        dirname = os.path.join(testcase_dir, dirname)
        os.system("mkdir %s" %(dirname))
        os.system("cp %s %s" %(config_map["@CONFIG_FILE@"], os.path.join(dirname, "config")))
        os.system("mv %s %s" %(struct_file, os.path.join(dirname, "struct")))


def gen_var_def(key, config_map):
    content = config_map[key]
    content = content.strip("(").strip(")")
    parts = content.split(",")
    _type = parts[0].strip()
    _name = parts[1].strip()
    _start = int(parts[2].strip().split("-")[0])
    _end = int(parts[2].strip().split("-")[1])
    _range = _end - _start
    def_str = _type + " " + _name + " = "
    if (_type == TYPE_UNSIGNED_CHAR):
        def_str = def_str + "input[%d];\n"%(_start)
    elif (_type == TYPE_UNSIGNED_INT):
        def_str = def_str + (FUN_READ_UNSIGNED_INT16 if _range==2 else FUN_READ_UNSIGNED_INT32) + "(&input[%d]);\n"%(_start)
    elif (_type == TYPE_UNSIGNED_CHAR_P):
        def_str = def_str + "&input[%d];\n" %(_start)
    return def_str


def gen_testcase(dirname, template_file):
    config_file = os.path.join(dirname, "config")
    struct_file = os.path.join(dirname, "struct")
    config_map = parse_config(config_file)
    # gen seed
    size = int(config_map["@INPUT_SIZE@"])
    content = ""
    for i in range(0, size):
        content = content + "0"
    # poc bytes buffer
    poc = bytearray(content)
    with open(os.path.join(dirname, "seed"), "w") as fp:
        fp.write(content)
    # gen src
    src = ""
    with open(template_file) as fp:
        src = fp.read()
    src = src.replace("@INPUT_SIZE@", str(size))
    # gen defs
    defs = ""
    for key in config_map.keys():
        if key.startswith("@VAR"):
            defs = defs + gen_var_def(key, config_map)
        elif key.startswith("@EXTRA_VARS"):
            defs = defs + config_map[key] + "\n"
    # insert defs
    src = src.replace("@VARDEFS@", defs)
    
    # gen conditions, and gen poc
    with open(struct_file) as fp:
        content = fp.readlines()
    conditions_str = ""
    conditions_str_kai = ""
    bug_trigger_space = ""
    bug_seen = False
    bug_kai = False
    dirname_kai = dirname + "_kai"
    bug_related_constraints_num = 0
    bug_unrelated_constraints_num = 0
    for line_num in range(0, len(content)):
        line = content[line_num].strip()
        if line.startswith("#"):
            continue
        elif line.startswith("@BUG@"):
            conditions_str = conditions_str + "bug();\n"
            bug_seen = True
        elif line.startswith("@CONDITION"):
            if content[line_num+1].strip().startswith("@BUG@"):
                bug_kai = True
            if not bug_seen:
                bug_related_constraints_num += 1
            else:
                bug_unrelated_constraints_num += 1

            # gen poc, get the range of the tainted variable
            variable = "@" + line.split(":")[-1].strip()
            variable = config_map[variable]
            _range = variable.strip().strip("(").strip(")").split(",")[-1].strip()
            _start = int(_range.split("-")[0])
            _end = int(_range.split("-")[1])
            
            value = config_map[line]
            value = value.strip("(").strip(")").split(",")
            op = value[1].strip()
            if op == "==":
                if bug_kai:
                    lower = value[2].strip()
                    lower = int(lower, 16) - 1
                    upper = lower + 2
                    conditions_str_kai = conditions_str + "bug2(%s, %d, %d);\n"%(value[0].strip(), lower, upper)

                conditions_str = conditions_str + "if (%s == %s) {\n" %(value[0].strip(), value[2].strip())
                conditions_str = conditions_str + "//@NOISE@\n"
                bug_trigger_space = bug_trigger_space + value[3].strip() + "*"
                # gen poc
                int_arr = to_intarray(value[2].strip())
                blank = (_end-_start) - len(int_arr)
                for i in range(0, blank):
                    poc[_start + i] = 0
                for i in range(_start+blank, _end):
                    poc[i] = int_arr[i-_start-blank]
            elif op == "&&":
                if bug_kai:
                    lower = value[2].strip()
                    lower = int(lower, 16)
                    upper = value[3].strip()
                    upper = int(upper, 16)
                    conditions_str_kai = conditions_str + "bug2(%s, %d, %d);\n"%(value[0].strip(), lower, upper)

                conditions_str = conditions_str + "if (%s > %s && %s < %s) {\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip())
                conditions_str = conditions_str + "//@NOISE@\n"
                bug_trigger_space = bug_trigger_space + value[4].strip() + "*"
                # gen poc
                int_arr = to_intarray(value[2].strip())
                int_arr[-1] = int_arr[-1] + 1
                blank = (_end-_start) - len(int_arr)
                for i in range(0, blank):
                    poc[_start + i] = 0
                for i in range(_start+blank, _end):
                    poc[i] = int_arr[i-_start-blank]
            elif op == "strncmp" or op == "memcmp":
                conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0) {\n" %(op, value[0].strip(), value[2].strip(), value[3].strip())
                conditions_str = conditions_str + "//@NOISE@\n"
                bug_trigger_space = bug_trigger_space + value[4].strip() + "*"
                # gen poc
                if op == "strncmp":
                    const_str = value[2].strip().strip("\"")
                    for i in range(_start, _end):
                        poc[i] = ord(const_str[i-_start])
                elif op == "memcmp":
                    extra_var = ""
                    for key in config_map.keys():
                        if key.startswith("@EXTRA_VAR"):
                            extra_var = config_map[key]
                            if extra_var.find(value[2].strip()) >= 0:
                                break
                    extra_var = extra_var.split("[]=")[-1].strip("{").strip(";").strip("}").split(",")
                    hex_str = "0x"
                    for i in range(0, len(extra_var)):
                        tmp = extra_var[i]
                        tmp = tmp[2:]
                        if len(tmp) <= 1:
                            tmp = "0" + tmp
                        hex_str += tmp
                    int_arr = to_intarray(hex_str)
                    for i in range(_start, _end):
                        poc[i] = int_arr[i-_start]
        elif line.startswith("@ELSE@"):
            conditions_str = conditions_str + "} else {\n" + "//@NOISE@\n" + "}\n"
            if conditions_str_kai and bug_kai:
                # skip the first else
                bug_kai = False
                continue
            elif conditions_str_kai and not bug_kai:
                conditions_str_kai = conditions_str_kai + "} else {\n" + "//@NOISE@\n" + "}\n"
            elif not conditions_str_kai and not bug_kai:
                continue

    # gen hardness
    hardness_file = os.path.join(dirname, "hardness")
    hardness = ""
    hardness = hardness + "INPUT_BYTES=%s" %(config_map["@INPUT_SIZE@"].strip()) + "\n"
    hardness = hardness + "TAINTED_BYTES=%s" %(config_map["@TAINTED_SIZE@"].strip()) + "\n"
    hardness = hardness + "TAINTED_VARIABLES_NUM=%s" %(config_map["@TAINTED_VAR_NUM@"].strip()) + "\n"
    hardness = hardness + "BUG_TRIGGERING_SPACE=%s" %(bug_trigger_space[:-1]) + "\n"
    hardness = hardness + "CONDITIONAL_BRANCH_STMT_NUM=%d" %(bug_related_constraints_num) + "\n"
    hardness = hardness + "BUG_UNRELATED_CONSTRAINTS_NUM=%d" %(bug_unrelated_constraints_num) + "\n"
    with open(hardness_file, "w") as fp:
        fp.write(hardness)
    # gen poc
    bb = bytearray(poc)
    poc_file = os.path.join(dirname, "poc")
    with open(poc_file, "wb") as fp:
        fp.write(poc)
    # gen Makefile
    os.system("cp Makefile %s" %(dirname))

    src_1 = src.replace("@INSERTION@", conditions_str)
    src_file = os.path.join(dirname, dirname.strip("/").split("/")[-1] + ".c")
    with open(src_file, "w") as fp:
        fp.write(src_1)

    if conditions_str_kai:
        os.system("cp -r %s %s" %(dirname, dirname_kai))
        os.system("rm %s" %(os.path.join(dirname_kai, dirname.strip("/").split("/")[-1] + ".c")))
        src_kai = src.replace("@INSERTION@", conditions_str_kai)
        src_file = os.path.join(dirname_kai, dirname_kai.strip("/").split("/")[-1] + ".c")
        with open(src_file, "w") as fp:
            fp.write(src_kai)


def parse_config(config_file):
    config_map = {}
    config_content = ""
    with open(config_file) as fp:
        config_content = fp.read()
    config_contents = config_content.split('\n')
    for config_content in config_contents:
        config_content = config_content.strip()
        if len(config_content) == 0 or config_content.startswith('#'):
            continue
        index = config_content.find("@=")
        key = config_content[:index+1]
        value = config_content[index+2:]
        config_map[key]=value
    return config_map


def parse_structure(struct_file, configurations):
    content = ""
    with open(struct_file) as struct:
        content = struct.read()
    return replace(content, configurations)


if __name__ == '__main__':
    config_maps_4_4 = gen_config(4, 4)
    config_maps_8_4 = gen_config(8, 4)
    config_maps_8_8 = gen_config(8, 8)
    #config_maps_16_4 = gen_config(16, 4)
    #config_maps_16_8 = gen_config(16, 8)
    #config_maps_16_16 = gen_config(16, 16)
    #config_maps_32_16 = gen_config(32, 16)

    #for config_map in config_maps_32_16:
    #    gen_struct(config_map)
    for config_map in config_maps_4_4:
        gen_struct(config_map)
    for config_map in config_maps_8_4:
        gen_struct(config_map)
    for config_map in config_maps_8_8:
        gen_struct(config_map)
    #for config_map in config_maps_16_4:
    #    gen_struct(config_map)
    #for config_map in config_maps_16_8:
    #    gen_struct(config_map)
    #for config_map in config_maps_16_16:
    #    gen_struct(config_map)

    print("start gen testcases")
    for testcase in os.listdir(testcase_dir):
        gen_testcase(os.path.join(testcase_dir, testcase), "template")
    """
    target_dir = sys.argv[1]
    #src_file = "./main.c"
    src_file = os.path.join(target_dir, "template")
    config_file = os.path.join(target_dir, "config")
    struct_file = os.path.join(target_dir, "struct")
    src_buf = gen_src(src_file, config_file, struct_file)
    target_src = os.path.join(target_dir, target_dir.strip("/").split("/")[-1]+".c")
    print(target_src)
    with open(target_src, 'w') as fp:
        fp.write(src_buf)
    """
