# -*- coding: utf-8 -*-

# log trace
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


class Config():
    def __init__(self, config_file=None, config_map=None):
        self.config_file = config_file
        self.config_map = None
        self.vars = None
        self.ut_vars = None
        if config_map:
            self.config_map = config_map
        elif self.config_file:
            self.config_map = self.parse_config(self.config_file)

    def parse_config(self, config_file):
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


    def get_vars(self, UTVAR=False):
        varlst = []
        for key in self.config_map.keys():
            ok = False
            if not UTVAR and key.startswith("@VAR"):
                ok = True
            elif UTVAR and key.startswith("@UTVAR"):
                ok = True
            if ok:
                var = Var(self.config_map)
                content = self.config_map[key]
                content = content.strip("(").strip(")")
                parts = content.split(",")
                var.type = parts[0].strip()
                var.name = parts[1].strip()
                _start = int(parts[2].strip().split("-")[0])
                _end = int(parts[2].strip().split("-")[1])
                var.bytes = _end - _start
                varlst.append(var)
        return varlst


# 父类
class Template():
    # 例如 @NOISE:UTVAR4@=(UTVAR4, &&, 242, 244, 0x1)
    # key为@NOISE:UTVAR4@
    # value为(UTVAR4, &&, 242, 244, 0x1)
    def __init__(self, config_file):
        self.config = None
        if type(config_file) == type(str):
            self.config = Config(config_file=config_file)
        else:
            self.config = Config(config_map=config_file)
        self.raw_str = ""
        self.key = None
        self.value = None

    def set_raw_str(self, raw):
        self.raw_str = raw
        index = raw.find("@=")
        self.key = raw[:index+1]
        self.value = raw[index+2:]

    # 解析，例如解析(UTVAR4, &&, 242, 244, 0x1)
    def parse_value(self):
        pass

    # 生成源代码
    def gen_code(self):
        return ""

# 子类1 Var 代表变量定义
class Var(Template):
    TYPE_UNSIGNED_CHAR = "unsigned char"
    TYPE_UNSIGNED_CHAR_P = "unsigned char*"
    TYPE_CHAR = "char"
    TYPE_CHAR_P = "char*"
    TYPE_UNSIGNED_INT = "unsigned int"
    TYPE_UNSIGNED_INT_P = "unsigned int*"
    TYPE_BOOL = "bool"
    TYPE_BOOL_P = "bool*"
    TYPE_LONG = "long"
    TYPE_LONG_P = "long*"
    TYPE_DOUBLE = "double"
    TYPE_DOUBLE_P = "double*"
    def __init__(self, config_file):
        Template.__init__(self, config_file)
        self.type = ""
        self.bytes = -1
        self.name = ""

    # 变量类型是否为数字类型
    def is_numeric(self):
        n = False
        if self.type == Var.TYPE_UNSIGNED_CHAR:
            n = True
        if self.type == Var.TYPE_CHAR:
            n = True
        if self.type == Var.TYPE_UNSIGNED_INT:
            n = True
        if self.type == Var.TYPE_BOOL:
            n = True
        if self.type == Var.TYPE_LONG:
            n = True
        if self.type == Var.TYPE_DOUBLE:
            n = True
        return n


# 子类2 Condition 代表if条件语句
class Condition(Template):

    def __init__(self, config_file):
        Template.__init__(self, config_file)
        self.var_name = ""
        self.op = "" # '==', '&&', 'strncmp', 'memcmp'
        self.lower = ""
        self.upper = ""
        self.trigger_space = "" # strigger space
        pass


    def parse_value(self):
        parts = self.value.strip("(").strip(")").split(",")
        self.var_name = parts[0].strip()
        self.op = parts[1].strip()
        if self.op == "==":
            self.lower = parts[2].strip()
            self.upper = parts[2].strip()
            self.trigger_space = '0x01'
        elif self.op == "&&":
            self.lower = parts[2].strip()
            self.upper = parts[3].strip()
            self.trigger_space = parts[4].strip()
        elif self.op == "strncmp" or self.op == "memcmp":
            self.lower = parts[2].strip()
            self.upper = parts[3].strip() # length
            self.trigger_space = '0x01'

    def gen_code(self):
        if not self.raw_str:
            return ""
        self.parse_value()
        src = ""
        if self.op == "==":
            src = "if(%s==%s)"%(self.var_name, self.lower)
        elif self.op == "&&":
            src = "if(%s>=%s && %s<%s)"%(self.var_name, self.lower, self.var_name, self.upper)
        elif self.op == "strncmp" or self.op == "memcmp":
            src = "if(%s(%s, %s, %s))"%(self.op, self.var_name, self.lower, self.upper)
        return src


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


# one byte per integer, n bytes hex string corresponds to n integers array
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


def _gen_path(conditions):
    if len(conditions.keys()) <= 1:
        result_paths = []
        _keys = list(conditions.keys())
        k = _keys[0]
        for one in conditions[k]:
            result_paths.append([one])
        return result_paths
    else:
        _keys = list(conditions.keys())
        k = _keys[0]
        cond_ids = conditions.pop(k)
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


def gen_noise(testcase):
    config_file = os.path.join(testcase, "config")
    config_map = parse_config(config_file)
    noise_cond_map = __gen_noise_from_config(config_map)
    noise_src = __gen_noise_code(noise_cond_map, config_map)
    new_content = ""
    for one in os.listdir(testcase):
        if one.startswith("IS") and one.endswith(".c"):
            src_file = os.path.join(testcase, one)
            with open(src_file) as fp:
                content = fp.read()
                parts = content.split("//@NOISE@")
                for i in range(0, len(parts)-1):
                    new_content += parts[i]
                new_content += noise_src
                new_content += parts[-1]
            with open(src_file, 'w') as fp:
                fp.write(new_content)
            break


def __gen_noise_code(noise_cond_map, config_map):
    vname_src_map = {}
    src = ""
    for variable in noise_cond_map.keys():
        conditions = noise_cond_map[variable]
        vname_src_map[variable] = []
        for condition in conditions:
            cond = Condition(config_map)
            cond.set_raw_str(condition)
            src += cond.gen_code()
            src +=  "\n" + "printf(\"%s\\n\");\n"%(hash(src))
    return src


def __gen_noise_from_config(config_map):
    config = Config(config_map=config_map)
    utvs = config.get_vars(UTVAR=True)
    cond_map = {}
    for v in utvs:
        conditions = []
        # 对于指针、字符串类型的变量，跳过
        if not v.is_numeric():
            continue
        # 如果是数字类型的（暂时限定为整型），则它的取值范围是...
        _max = pow(2, v.bytes*8)-1
        step = 0
        if _max > 100:
            step = int(_max/100)
        else:
            step = -1
        op = "=="
        cond_str = ""
        if step > 1:
            op = "&&"
        value = 0
        while value < _max:
            if op == "==":
                cond_str = "@NOISE:%s@=(%s, %s, %d, %s)" %(v.name, v.name, op, value, hex(1))
                value = value + 1
            elif op == "&&":
                cond_str = "@NOISE:%s@=(%s, %s, %d, %d, %s)" %(v.name, v.name, op, value, value+step, hex(step-1))
                value = value + step
            conditions.append(cond_str)
        cond_map[v.name] = conditions
    return cond_map


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
    def_str = def_str + "int %s_size = %d;\n" %(_name, _range);
    return def_str


# 往struct_file的条件语句上添加妨碍特征，数量为inum个
# 妨碍特征可以为 "IDF1"（简单的隐式数据流） "IDF2"（复杂一点的隐式数据流） "CRC"
def add_hampering_feature(config_file, struct_file, hampering_feature="IDF1", inum=-1):
    config_map = parse_config(config_file)
    content = ""
    with open(struct_file) as fp:
        content = fp.read()
    lines = content.split("\n")
    cond_linenums = []
    for i in range(0, len(lines)):
        if lines[i].startswith("#"):
            continue
        if hampering_feature == "CRC":
            #排除条件是 && 的条件，因为CRC只能改造‘==’和‘strncmp’，memcmp因为难以处理常量CRC值，暂时搁置
            line = lines[i].strip().split('$')[0].strip()
            if line.startswith("@CONDITION"):
                if config_map[line].split(',')[1].strip() == "&&" or config_map[line].find("memcmp") >= 0:
                    continue
        if hampering_feature == "gaussian":
            #排除条件是strncmp和memcmp的
            line = lines[i].strip().split('$')[0].strip()
            if line.startswith("@CONDITION"):
                if config_map[line].find("strncmp") >= 0 or config_map[line].find("memcmp") >= 0:
                    continue
        if lines[i].startswith("@CONDITION") and lines[i].find("$NOISE$") < 0:
            cond_linenums.append(i)

    implicit_conds = []
    if inum > 0 and inum <= len(cond_linenums):
        for i in range(0, inum):
            index = int(len(cond_linenums)*random.random())
            implicit_conds.append(cond_linenums.pop(index))
    else:
        return None

    for i in range(0, len(implicit_conds)):
        linenum = implicit_conds[i]
        line = lines[linenum]
        if hampering_feature == "IDF1":
            lines[linenum] = line + "$IMPLICIT_DATAFLOW1$"
        elif hampering_feature == "IDF2":
            lines[linenum] = line + "$IMPLICIT_DATAFLOW2$"
        elif hampering_feature == "CRC":
            lines[linenum] = line + "$CRC$"
        elif  hampering_feature == "gaussian":
            lines[linenum] = line + "$GAUSSIAN$"
    content = ""
    for line in lines:
        content = content + line + "\n"
    return content


def _implicit_dataflow1(conditions_str, key, value, tmp_index, if_implicit_dataflow):
    op = value[1].strip()
    if if_implicit_dataflow:
        conditions_str = conditions_str + "int tmp%d = 0;\n" %(tmp_index)
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s)\n" %(value[0].strip(), value[2].strip())
        elif op == "&&":
            conditions_str = conditions_str + "if (%s >= %s && %s < %s)\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip())
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0)\n" %(op, value[0].strip(), value[2].strip(), value[3].strip())
        conditions_str = conditions_str + "tmp%d = 1;\n" %(tmp_index)
        conditions_str = conditions_str + "if (tmp%d == 1) {\nfputs(\"%s##\", fp);\n" %(tmp_index, key)
        tmp_index = tmp_index + 1
    else:
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), key)
        elif op == "&&":
            conditions_str = conditions_str + "if (%s >= %s && %s < %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip(), key)
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0) {\nfputs(\"%s##\", fp);\n" %(op, value[0].strip(), value[2].strip(), value[3].strip(), key)
    return conditions_str, tmp_index

def __gen_src_implicit_dataflow2(var_name, tmp_index, config_map):
    #int temp=0, temp2=0, ch=0; // used for implicit dataflow
    #char cc[var_name_size]
    #int VAR1_size=4; //代表VAR1变量的大小为4个字节
    var_size = var_name+"_size"
    var_type = config_map["@%s@"%(var_name)].strip("(").strip(")").split(",")[0].strip()
    src = "unsigned char cc%d[%s];\n" %(tmp_index, var_size)
    if(var_type == "unsigned char" or var_type == "unsigned int"):
        src = src + "for (i=0; i<%s; i++) {\n" %(var_size)
        src = src + "ch = 0;\ntemp = (%s>>i*8) & 0x000000FF;\nfor (int j=0; j<8; j++) {\n"%(var_name)
        src = src + "temp2 = temp & (1<<j);\nif (temp2!=0) ch |= 1<<j;\n}\n"
        src = src + "cc%d[%s-1-i] = ch;\n}\n"%(tmp_index, var_size)
        src = src + "ch = read_int(cc%d, %s);\n" %(tmp_index, var_size)
    elif(var_type == "unsigned char*"):
        src = src + "for (i=0; i<%s; i++) {\n" %(var_size)
        src = src + "ch = 0;\nfor (int j = 0; j<8; j++){\n"
        src = src + "temp = %s[i];\ntemp2 = temp & (1<<j);\nif (temp2 != 0) ch |= 1<<j;\n}\n"%(var_name)
        src = src + "cc%d[i] = ch;\n}\n" %(tmp_index)
    return src

def _implicit_dataflow2(conditions_str, key, value, tmp_index, if_implicit_dataflow, config_map):
    var_name = value[0];
    op = value[1].strip()
    if if_implicit_dataflow:
        src = __gen_src_implicit_dataflow2(var_name, tmp_index, config_map)
        conditions_str = conditions_str + src
        if op == "==":
            conditions_str = conditions_str + "if (ch == %s) {\nfputs(\"%s##\", fp);\n" %(value[2].strip(), key)
        elif op == "&&":
            conditions_str = conditions_str + "if (ch >= %s && ch < %s) {\nfputs(\"%s##\", fp);\n" %(value[2].strip(), value[3].strip(), key)
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(cc%d, %s, %s) == 0) {\nfputs(\"%s##\", fp);\n" %(op, tmp_index, value[2].strip(), value[3].strip(), key)
        tmp_index = tmp_index + 1
    else:
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), key)
        elif op == "&&":
            conditions_str = conditions_str + "if (%s >= %s && %s < %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip(), key)
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0) {\nfputs(\"%s##\", fp);\n" %(op, value[0].strip(), value[2].strip(), value[3].strip(), key)
    return  conditions_str, tmp_index

def _crc(conditions_str, key, value, val_size, tmp_index, if_crc, config_map):
    var_name = value[0];
    op = value[1].strip()
    if if_crc:
        bytes_num = 0
        if op == "==":
            conditions_str = conditions_str + "unsigned char* tmp%d = int2byte(%s, %s);\n" %(tmp_index, var_name, var_name+"_size")
            b_arr = (int(value[2].strip(), 16)).to_bytes(val_size, byteorder='big')
            crc_val = crc(b_arr, val_size)
            conditions_str = conditions_str + "if (crc(tmp%d, %s) == %d) {\nfputs(\"%s##\", fp);\n" %(tmp_index, var_name+"_size", crc_val, key)
            tmp_index = tmp_index + 1
        elif op == "strncmp":
            crc_val = crc(value[2].strip().strip('\"'), int(value[3].strip()))
            conditions_str = conditions_str + "if(crc(%s, %s) == %d) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), var_name+"_size", crc_val, key)
    else:
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), key)
        elif op == "&&":
            conditions_str = conditions_str + "if (%s >= %s && %s < %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip(), key)
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0) {\nfputs(\"%s##\", fp);\n" %(op, value[0].strip(), value[2].strip(), value[3].strip(), key)
    return conditions_str, tmp_index

def _gaussian(conditions_str, key, value, val_size, tmp_index, if_gaussian, config_map):
    var_name = value[0];
    op = value[1].strip()
    if if_gaussian:
        bytes_num = 0
        if op == "==":
            lower = int(value[2].strip(), 16) - 1
            upper = lower + 2
            conditions_str = conditions_str + "if (gaussian(%s, %s, %s) > 0) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), hex(lower), hex(upper), key)
        elif op == "&&":
            lower = int(value[2].strip(), 16)
            upper = int(value[3].strip(), 16)
            conditions_str = conditions_str + "if (gaussian(%s, %s, %s) > 0) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), hex(lower), hex(upper), key)
    else:
        if op == "==":
            conditions_str = conditions_str + "if (%s == %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), key)
        elif op == "&&":
            conditions_str = conditions_str + "if (%s >= %s && %s < %s) {\nfputs(\"%s##\", fp);\n" %(value[0].strip(), value[2].strip(), value[0].strip(), value[3].strip(), key)
        elif op == "strncmp" or op == "memcmp":
            conditions_str = conditions_str + "if (%s(%s, %s, %s) == 0) {\nfputs(\"%s##\", fp);\n" %(op, value[0].strip(), value[2].strip(), value[3].strip(), key)
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
    poc = bytearray(content, 'utf-8')
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
        if key.startswith("@VAR") or key.startswith("@UTVAR"):
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
    tmp_index = 0; #用于隐式数据流的临时变量之编号
    dirname_kai = dirname + "_kai"
    bug_related_constraints_num = 0
    bug_unrelated_constraints_num = 0
    for line_num in range(0, len(content)):
        implicit_dataflow1 = False #是否使用隐式数据流，类型1
        implicit_dataflow2 = False #是否使用隐式数据流，类型2
        crc = False # 是否使用crc对抗符号执行
        gaussian = False # 是否使用高斯函数对抗符号执行
        line = content[line_num].strip()
        if line.startswith("#"):
            continue
        elif line.startswith("@BUG@"):
            conditions_str = conditions_str + "fputs(\"\\n\", fp);\nfclose(fp);\nfp = NULL;\nbug();\n"
            bug_seen = True
        elif line.startswith("@CONDITION"):
            if content[line_num+1].strip().startswith("@BUG@"):
                bug_kai = True #说明这个condition紧挨着@BUG@，是可以被替换成高斯函数的
            if line.find("$IMPLICIT_DATAFLOW1$") >= 0:
                implicit_dataflow1 = True
                implicit_dataflow2 = False
            elif line.find("$IMPLICIT_DATAFLOW2$") >= 0:
                implicit_dataflow1 = False
                implicit_dataflow2 = True
            elif line.find("$CRC$") >= 0:
                crc = True
            elif line.find("$GAUSSIAN$") >= 0:
                gaussian = True

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
            _size = _end - _start # 变量所占字节数
            
            value = config_map[line.split("$")[0]]
            value = value.strip("(").strip(")").split(",")
            op = value[1].strip()
            if op == "==":
                if bug_kai:
                    lower = value[2].strip()
                    lower = int(lower, 16) - 1
                    upper = lower + 2
                    conditions_str_kai = conditions_str + "fputs(\"\\n\", fp);\nfclose(fp);\nfp = NULL;\nbug2(%s, %d, %d);\n"%(value[0].strip(), lower, upper)
                if implicit_dataflow2:
                    conditions_str, tmp_index = _implicit_dataflow2(conditions_str, line.strip(), value, tmp_index, implicit_dataflow2, config_map)
                elif crc:
                    conditions_str, tmp_index = _crc(conditions_str, line.strip(), value, _size, tmp_index, crc, config_map)
                elif gaussian:
                    conditions_str, tmp_index = _gaussian(conditions_str, line.strip(), value, _size, tmp_index, gaussian, config_map)
                else:
                    conditions_str, tmp_index = _implicit_dataflow1(conditions_str, line.strip(), value, tmp_index, implicit_dataflow1)
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
                    conditions_str_kai = conditions_str + "fputs(\"\\n\", fp);\nfclose(fp);\nfp = NULL;\nbug2(%s, %d, %d);\n"%(value[0].strip(), lower, upper)

                if implicit_dataflow2:
                    conditions_str, tmp_index = _implicit_dataflow2(conditions_str, line.strip(), value, tmp_index, implicit_dataflow2, config_map)
                elif gaussian:
                    conditions_str, tmp_index = _gaussian(conditions_str, line.strip(), value, _size, tmp_index, gaussian, config_map)
                else:
                    conditions_str, tmp_index = _implicit_dataflow1(conditions_str, line.strip(), value, tmp_index, implicit_dataflow1)

                conditions_str = conditions_str + "//@NOISE@\n"
                bug_trigger_space = bug_trigger_space + value[4].strip() + "*"
                # gen poc
                int_arr = to_intarray(value[2].strip())
                #int_arr[-1] = int_arr[-1] + 1
                int_arr[-1] = int_arr[-1]
                blank = (_end-_start) - len(int_arr)
                for i in range(0, blank):
                    poc[_start + i] = 0
                for i in range(_start+blank, _end):
                    poc[i] = int_arr[i-_start-blank]
            elif op == "strncmp" or op == "memcmp":
                if implicit_dataflow2:
                    conditions_str, tmp_index = _implicit_dataflow2(conditions_str, line.strip(), value, tmp_index, implicit_dataflow2, config_map)
                elif crc:
                    conditions_str, tmp_index = _crc(conditions_str, line.strip(), value, _size, tmp_index, crc, config_map)
                else:
                    conditions_str, tmp_index = _implicit_dataflow1(conditions_str, line.strip(), value, tmp_index, implicit_dataflow1)
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
            conditions_str = conditions_str + "} else {\n" + "//@NOISE@\nfputs(\"%s##\", fp);\n"%(line.strip()) + "}\n"
            if conditions_str_kai and bug_kai:
                # skip the first else
                bug_kai = False
                continue
            elif conditions_str_kai and not bug_kai:
                conditions_str_kai = conditions_str_kai + "} else {\n" + "//@NOISE@\nfputs(\"%s##\", fp);\n"%(line.strip()) + "}\n"
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

    src = src.replace("@TRACE_FILE@", os.path.basename(dirname).strip())
    src_1 = src.replace("@INSERTION@", conditions_str)
    src_file = os.path.join(dirname, dirname.strip("/").split("/")[-1] + ".c")
    with open(src_file, "w") as fp:
        fp.write(src_1)

    if conditions_str_kai and dirname.find("kai") < 0 and dirname.find("IDF") < 0 and dirname.find("CRC") < 0 and dirname.find("NOISE") < 0 and dirname.find("gaussian") < 0:
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

def gen_testcases_noise_path(testcase_dir):
    testcase_dir_lst = []
    noise_testcase_dir_lst = []
    for one in os.listdir(testcase_dir):
        if one == "lib" or one == "include" or one.find("_kai") >= 0:
            continue
        testcase_dir_lst.append(os.path.join(testcase_dir, one))
    for one in testcase_dir_lst:
        if one.find("_NOISE") >= 0:
            continue
        new_dir = one + "_NOISE"
        struct_file = os.path.join(one, "struct")
        config_file = os.path.join(one, "config")
        with open(config_file) as fp:
            content = fp.read()
            # 找不到untainted variables，跳过，不生成噪声路径
            if content.find("@UTVAR") < 0:
                continue
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.system("cp %s %s" %(struct_file, new_dir))
        os.system("cp %s %s" %(config_file, new_dir))
        noise_testcase_dir_lst.append(new_dir)
    return noise_testcase_dir_lst


# 修改struct文件，给样本增添隐式数据流
def gen_testcases_hampering_feature(testcase_dir, hampering_feature="IDF1"):
    testcase_dir_lst = []
    idf_testcase_dir_lst = []
    for one in os.listdir(testcase_dir):
        if one == "lib" or one == "include" or one.find("_kai") >= 0:
            continue
        testcase_dir_lst.append(os.path.join(testcase_dir, one))
    for one in testcase_dir_lst:
        # 跳过已经包含隐式数据流/CRC的样本
        if one.find("IDF") >= 0 or one.find("CRC") >= 0 or one.find("gaussian") >= 0:
            continue
        # copy config and struct
        if hampering_feature == "IDF1":
            new_dir = one + "_IDF1"
        elif hampering_feature == "CRC":
            new_dir = one + "_CRC"
        elif hampering_feature == "gaussian":
            new_dir = one + "_gaussian"
        struct_file = os.path.join(one, "struct")
        config_file = os.path.join(one, "config")
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.system("cp %s %s" %(struct_file, new_dir))
        os.system("cp %s %s" %(config_file, new_dir))
        if hampering_feature == "IDF1":
            content = add_hampering_feature(config_file, struct_file, hampering_feature="IDF1", inum=1)
        elif hampering_feature == "CRC":
            content = add_hampering_feature(config_file, struct_file, hampering_feature="CRC", inum=1)
        elif hampering_feature == "gaussian":
            content = add_hampering_feature(config_file, struct_file, hampering_feature="gaussian", inum=1)
        if not content:
            # 无法生成带有妨碍特征的struct，删除文件夹，然后处理下一个
            os.system("rm -rf %s" %(new_dir))
            continue
        with open(os.path.join(new_dir, "struct"), "w") as fp:
            fp.write(content)
        idf_testcase_dir_lst.append(new_dir)
    # 返回样本路径列表
    return idf_testcase_dir_lst

# 把IDF1样本的struct中的$IMPLICIT_DATAFLOW1$改成$IMPLICIT_DATAFLOW2$即可
def gen_testcases_implicit_dataflow2(testcase_dir):
    IDF1 = []
    IDF2 = []
    for one in os.listdir(testcase_dir):
        if not one.endswith("_IDF1"):
            continue
        IDF1.append(os.path.join(testcase_dir, one))
    for one in IDF1:
        # 复制
        new_dir = one[:-1]+"2"
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        struct_file = os.path.join(one, "struct")
        new_struct_file = os.path.join(new_dir, "struct")
        config_file = os.path.join(one, "config")
        os.system("cp %s %s" %(struct_file, new_dir))
        os.system("cp %s %s" %(config_file, new_dir))
        # 替换原strcut中的$IMPLICIT_DATAFLOW1$
        with open(struct_file) as fp:
            content = fp.read()
            content = content.replace("IMPLICIT_DATAFLOW1", "IMPLICIT_DATAFLOW2")
            with open(new_struct_file, "w") as wp:
                wp.write(content)
        IDF2.append(new_dir)
    # 返回样本路径列表
    return IDF2

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", help="input configuration file")
    parser.add_argument("-g", "--generate", dest="gen", help="[idf1|idf2|crc|noise|gaussian]")
    parser.add_argument("-t", "--target", dest="target", help="target directory")
    parser.add_argument("-dt", "--directtarget", dest="directtarget", help="target testcase directory")
    args = parser.parse_args()

    if args.directtarget:
        gen_testcase(args.directtarget, "template2")
    
    if args.config:
        config_map = parse_config(args.config)
        basename = os.path.basename(args.config)
        os.system("cp %s %s" %(args.config, basename))
        testcases_dir = gen_struct(config_map)
        for testcase in testcases_dir:
            gen_testcase(testcase, "template2")
        os.system("rm %s" %(basename))

    if args.gen == "idf1":
        idf_testcases = gen_testcases_hampering_feature(args.target, hampering_feature="IDF1")
        for testcase in idf_testcases:
            gen_testcase(testcase, "template2")

    if args.gen == "idf2":
        idf_testcases = gen_testcases_implicit_dataflow2(args.target)
        for testcase in idf_testcases:
            gen_testcase(testcase, "template2")

    if args.gen == "crc":
        testcases = gen_testcases_hampering_feature(args.target, hampering_feature="CRC")
        for testcase in testcases:
            gen_testcase(testcase, "template2")

    if args.gen == "gaussian":
        testcases = gen_testcases_hampering_feature(args.target, hampering_feature="gaussian")
        for testcase in testcases:
            gen_testcase(testcase, "template2")

    if args.gen == "noise":
        noise_testcases = gen_testcases_noise_path(args.target)
        for testcase in noise_testcases:
            gen_testcase(testcase, "template2")
            gen_noise(testcase)
