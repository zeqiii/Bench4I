# Bench4I
Code generator that constructs benchmarks for interpretable evaluation of fuzz testing.

# Introduction
`template2` is a code template for generating C code.
`Bench4I` is a pre-generated benchmark.
`Makefile` is a universal Makefile for all generated target programs.

# Usage
Run `python gen_config_rand.py` to generate config files. The generated config files are in `configs` directory.

Run `python gen.py -c CONFIG` to generate original target programs. For example: `python gen.py -c configs/IS8_TS8_TV1.conf`, the generated target programs are in `testcases` directory.

Run `python3 gen.py -g FEATURE -t TARGET_DIR` to add fuzzing-hampering features to the target programs in `TARGET_DIR`. For example: `python3 gen.py -g crc -t testcases` will add CRC check sum to the original target programs in directory `testcases` .

Run `python gen_seeds.py TARGET_DIR` to genenerate seed files for the target programs in directory `TARGET_DIR`. For example: `python gen_seeds.py testcases` will generate seed files for every target program in `testcases`.

