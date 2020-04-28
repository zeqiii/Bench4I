#include "ebench.h"

// hide this control flow in this library
int return_param(unsigned int lower, unsigned int upper, unsigned int input)
{
    if (input < lower || input >= upper)
        return 0;
    else
        return 1;
}

// hidden in this library, dataflow from input to value
int implicit_dataflow(unsigned int input, unsigned char* value) {
    value[3] = input;
    value[2] = input >> 8;
    value[1] = input >> 16;
    value[0] = input >> 24;
    return 0;
}
