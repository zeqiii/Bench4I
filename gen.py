# -*- coding: utf-8 -*-
import os, sys, random, string
import numpy as np
import argparse

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

# one byte per integer, n bytes hex string corresponds to n integers array
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
    testcases_dir = []
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
        testcases_dir.append(dirname)
    return testcases_dir


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


# 往struct_file里添加隐形数据流，数量为inum个
def add_implicit_dataflow(struct_file, inum=-1):
    content = ""
    with open(struct_file) as fp:
        content = fp.read()
    lines = content.split("\n")
    cond_linenums = []
    for i in range(0, len(lines)):
        if lines[i].startswith("#"):
            continue
        if lines[i].startswith("@CONDITION") and lines[i].find("$NOISE$") < 0:
            cond_linenums.append(i)

    implicit_conds = []
    if inum > 0 and inum <= len(cond_linenums):
        for i in range(0, inum):
            index = int(len(cond_linenums)*random.random())
            implicit_conds.append(cond_linenums.pop(index))
    for i in range(0, len(implicit_conds)):
        linenum = implicit_conds[i]
        line = lines[linenum]
        lines[linenum] = line + "$IMPLICIT_DATAFLOW$"
    content = ""
    for line in lines:
        content = content + line + "\n"
    return content


def _implicit_dataflow(conditions_str, value, tmp_index, if_implicit_dataflow, op):
    if if_implicit_dataflow:
        conditions_str = conditions_str + "int tmp%d = 0;\n" %(tmp_index)
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s)\n" %(value[0].strip(), value[2].strip())
        elif op == "&&":
            conditions_str = conditions_str + "if (%s > %s && %s < %s)\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip())
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0)\n" %(op, value[0].strip(), value[2].strip(), value[3].strip())
        conditions_str = conditions_str + "tmp%d = 1;\n" %(tmp_index)
        conditions_str = conditions_str + "if (tmp%d == 1) {\n" %(tmp_index)
        tmp_index = tmp_index + 1
    else:
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s) {\n" %(value[0].strip(), value[2].strip())
        elif op == "&&":
            conditions_str = conditions_str + "if (%s > %s && %s < %s) {\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip())
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0) {\n" %(op, value[0].strip(), value[2].strip(), value[3].strip())
    return conditions_str, tmp_index


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
    
    # gen conditions, and gen poc 解析struct文件，生成代码
    with open(struct_file) as fp:
        content = fp.readlines()
    conditions_str = ""     # 原始语句
    conditions_str_kai = "" # 使用高斯函数代替判断语句
    bug_trigger_space = ""
    bug_seen = False #是否已经处理了@BUG@标签
    bug_kai = False  #是否使用高斯函数代替判断语句
    implicit_dataflow = False #是否使用隐式数据流
    tmp_index = 0; #用于隐式数据流的临时变量之编号
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
                bug_kai = True #说明这个condition紧挨着@BUG@，是可以被替换成高斯函数的
            if line.find("$IMPLICIT_DATAFLOW$") >= 0:
                implicit_dataflow = True
            else:
                implicit_dataflow = False
            if not bug_seen:
                bug_related_constraints_num += 1
            else:
                bug_unrelated_constraints_num += 1

            # gen poc, get the range of the tainted variable
            variable = "@" + line.split(":")[-1].strip().split("$")[0]
            variable = config_map[variable]
            _range = variable.strip().strip("(").strip(")").split(",")[-1].strip()
            _start = int(_range.split("-")[0])
            _end = int(_range.split("-")[1])
            
            value = config_map[line.split("$")[0]]
            value = value.strip("(").strip(")").split(",")
            op = value[1].strip()
            if op == "==":
                if bug_kai:
                    lower = value[2].strip()
                    lower = int(lower, 16) - 1
                    upper = lower + 2
                    conditions_str_kai = conditions_str + "bug2(%s, %d, %d);\n"%(value[0].strip(), lower, upper)
                conditions_str, tmp_index = _implicit_dataflow(conditions_str, value, tmp_index, implicit_dataflow, op)
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

                conditions_str, tmp_index = _implicit_dataflow(conditions_str, value, tmp_index, implicit_dataflow, op)
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
                conditions_str, tmp_index = _implicit_dataflow(conditions_str, value, tmp_index, implicit_dataflow, op)
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

    if conditions_str_kai and dirname.find("_kai") < 0 and dirname.find("_IDF") < 0:
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

#===================================
# 自定义的样本生成函数，非通用功能 =
#===================================

# 修改struct文件，给样本增添隐式数据流
def gen_testcases_implicit_dataflow(testcase_dir):
    testcase_dir_lst = []
    idf_testcase_dir_lst = []
    for one in os.listdir(testcase_dir):
        if one == "lib" or one == "include" or one.find("_kai") >= 0:
            continue
        testcase_dir_lst.append(os.path.join(testcase_dir, one))
    for one in testcase_dir_lst:
        # 跳过已经包含隐式数据流的样本
        if one.find("_IDF") >= 0:
            continue
        # copy config and struct
        new_dir = one + "_IDF1"
        struct_file = os.path.join(one, "struct")
        config_file = os.path.join(one, "config")
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.system("cp %s %s" %(struct_file, new_dir))
        os.system("cp %s %s" %(config_file, new_dir))
        content = add_implicit_dataflow(struct_file, inum=1)
        with open(struct_file, "w") as fp:
            fp.write(content)
        idf_testcase_dir_lst.append(new_dir)
    # 返回样本路径列表
    return idf_testcase_dir_lst

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", help="input configuration file")
    parser.add_argument("-g", "--generate", dest="gen", help="[idf]:generate implicit dataflow")
    parser.add_argument("-t", "--target", dest="target", help="target directory")
    args = parser.parse_args()
    
    if args.config:
        config_map = parse_config(args.config)
        testcases_dir = gen_struct(config_map)
        for testcase in testcases_dir:
            gen_testcase(testcase, "template")

    if args.gen == "idf":
        idf_testcases = gen_testcases_implicit_dataflow(args.target)
        for testcase in idf_testcases:
            gen_testcase(testcase, "template")


    #config_maps_4_4 = gen_config(4, 4)
    #config_maps_8_4 = gen_config(8, 4)
    #config_maps_8_8 = gen_config(8, 8)
    #config_maps_16_4 = gen_config(16, 4)
    #config_maps_16_8 = gen_config(16, 8)
    #config_maps_16_16 = gen_config(16, 16)
    #config_maps_32_16 = gen_config(32, 16)

    #for config_map in config_maps_32_16:
    #    gen_struct(config_map)
    #for config_map in config_maps_4_4:
    #    gen_struct(config_map)
    #for config_map in config_maps_8_4:
    #    gen_struct(config_map)
    #for config_map in config_maps_8_8:
    #    gen_struct(config_map)
    #for config_map in config_maps_16_4:
    #    gen_struct(config_map)
    #for config_map in config_maps_16_8:
    #    gen_struct(config_map)
    #for config_map in config_maps_16_16:
    #    gen_struct(config_map)

    #print("start gen testcases")
    #for testcase in os.listdir(testcase_dir):
    #    gen_testcase(os.path.join(testcase_dir, testcase), "template")
