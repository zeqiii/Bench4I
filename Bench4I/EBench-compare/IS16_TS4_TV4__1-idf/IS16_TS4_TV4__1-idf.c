#include<sys/stat.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<fcntl.h>
#include <unistd.h>
#include <math.h>

// record execution trace
//// section of functional functions

unsigned int read_unsigned_int16(unsigned char *input) {
    unsigned int uint16;
    uint16 = input[0] << 8;
    uint16 = uint16 | input[1];
    return uint16;
}

unsigned int read_unsigned_int32(unsigned char *input) {
    unsigned int uint32;
    uint32 = input[0] << 24;
    uint32 = uint32 | input[1] << 16;
    uint32 = uint32 | input[2] << 8;
    uint32 = uint32 | input[3];
    return uint32;
}

unsigned int read_int(unsigned char *input, int size) {
    unsigned int result = 0;
    for (int i=0; i<size; i++)
        result = (result<<(8)) | input[i];
    return result;
}

unsigned char* int2byte(unsigned int input, unsigned int len) {
    unsigned char* a = (unsigned char*)malloc(len*sizeof(unsigned char));
    for(int i=0; i<len; i++) {
        *(a+len-i-1) = (input>>(i*8)) & 0xFF;
    }
    return a;
}

unsigned long crc(unsigned char* test, unsigned int len) {
    unsigned long temp = 0;
    unsigned int crc;
    unsigned char i;
    unsigned char *ptr = test;
    while( len-- ) {
        for(i = 0x80; i != 0; i = i >> 1) {
            temp = temp * 2;
            if((temp & 0x10000) != 0)
                temp = temp ^ 0x11021;
            if((*ptr & i) != 0)
                temp = temp ^ (0x10000 ^ 0x11021);
        }
        ptr++;
    }
    return temp;
}

// when input is in (lower, upper), return 1, else return 0
int gaussian(unsigned int input, unsigned int lower, unsigned int upper) {
    double m = ((double)lower + (double)upper) / 2.0;
    double exponent = -1.0 * ((lower-m)*(lower-m)) / ((lower-m)*(lower-m));
    double fx = exp(exponent);
    double a = 1.0 / fx;

    double exponent2 = -1.0 * ((input-m)*(input-m)) / ((lower-m)*(lower-m));
    double fx2 = a * exp(exponent2);
    return (int)fx2;
}

// custom comparing function
int ncmp(unsigned char* a, unsigned char* b, unsigned int n) {
    int i = 0;
    while(i < n) {
        if (a[i] == b[i])
            i++;
        else if (a[i] < b[i])
            return -1;
        else
            return 1;
    }
    return 0;
}

//// section of functional functions


//// section of bug functions

void bug() {
    // implement your own bug
    // bug will be triggered as long as the execution reaches to this
    char dst[64];
    char* src = (char*)malloc(65535*sizeof(char));
    memset(src, 'A', 65535);
    memcpy(dst, src, 65535); // potential flaw, overflow
    free(src);
    printf("%d\n", *(src)); // potential flaw, UAF
}

void bug2(unsigned int input, unsigned int lower, unsigned int upper) {
    // implement your own bug
    // bug will be triggered when the parameter is in a particular range: (lower, upper)
    char dst[64];
    char* src = (char*)malloc(128*sizeof(char));
    memset(src, 'A', 128);
    memcpy(dst, src, 64+input*gaussian(input, lower, upper)); // potential flaw, overflow
    free(src);
    if (gaussian(input, lower, upper) > 0)
        printf("%d\n", *(src)); // potential flaw, UAF
}

void bug3(unsigned int input, unsigned int lower, unsigned int upper) {
    // implement your own bug
    // bug will be triggered when input is in a particular range
    if (input > upper)
        return;
    char* src = (char*)malloc(lower*sizeof(char));
    char c;
    unsigned int i = 0;
    while(i < input) {
        i++;
        c = *(src + i);
        printf("%c\n", c);
    }
    free(src);
}

//// section of bug fucntions


//// section of main function

int main(int argc, char **argv) {

    //// common header
    FILE *fp;
    if ((fp = fopen("/dev/shm/IS16_TS4_TV4__1-idf", "a+")) == NULL)
        exit(0);

    unsigned char input[16];
    int i, fd, size, tmp;
    int temp=0, temp2=0, ch=0; // used for implicit dataflow
    struct stat s;
    if ((fd = open(argv[1], O_RDONLY)) == -1) {
        fputs("Failed to open file!\n", fp);
        exit(0);
    }
    fstat(fd, &s);
    size = s.st_size;
    if (size < 16) {
        fputs("Input size invalid!\n", fp);
        return -1;
    }
    read(fd, input, 16);
    //// common header

    //// variables
    unsigned int UTVAR4 = read_unsigned_int32(&input[3]);
int UTVAR4_size = 4;
unsigned int UTVAR5 = read_unsigned_int32(&input[7]);
int UTVAR5_size = 4;
unsigned char UTVAR1 = input[0];
int UTVAR1_size = 1;
unsigned char UTVAR6 = input[15];
int UTVAR6_size = 1;
unsigned char VAR1 = input[11];
int VAR1_size = 1;
unsigned char UTVAR2 = input[1];
int UTVAR2_size = 1;
unsigned char VAR4 = input[14];
int VAR4_size = 1;
unsigned char UTVAR3 = input[2];
int UTVAR3_size = 1;
unsigned char VAR3 = input[13];
int VAR3_size = 1;
unsigned char VAR2 = input[12];
int VAR2_size = 1;

    //// variables

    //// section of insertion
    unsigned char cc0[VAR1_size];
for (i=0; i<VAR1_size; i++) {
ch = 0;
temp = (VAR1>>i*8) & 0x000000FF;
for (int j=0; j<8; j++) {
temp2 = temp & (1<<j);
if (temp2!=0) ch |= 1<<j;
}
cc0[VAR1_size-1-i] = ch;
}
ch = read_int(cc0, VAR1_size);
if (ch == 0x2d) {
fputs("@CONDITION2:VAR1@$IMPLICIT_DATAFLOW2$##", fp);
//@NOISE@
unsigned char cc1[VAR2_size];
for (i=0; i<VAR2_size; i++) {
ch = 0;
temp = (VAR2>>i*8) & 0x000000FF;
for (int j=0; j<8; j++) {
temp2 = temp & (1<<j);
if (temp2!=0) ch |= 1<<j;
}
cc1[VAR2_size-1-i] = ch;
}
ch = read_int(cc1, VAR2_size);
if (ch == 0x4a) {
fputs("@CONDITION4:VAR2@$IMPLICIT_DATAFLOW2$##", fp);
//@NOISE@
unsigned char cc2[VAR3_size];
for (i=0; i<VAR3_size; i++) {
ch = 0;
temp = (VAR3>>i*8) & 0x000000FF;
for (int j=0; j<8; j++) {
temp2 = temp & (1<<j);
if (temp2!=0) ch |= 1<<j;
}
cc2[VAR3_size-1-i] = ch;
}
ch = read_int(cc2, VAR3_size);
if (ch == 0x37) {
fputs("@CONDITION1:VAR3@$IMPLICIT_DATAFLOW2$##", fp);
//@NOISE@
unsigned char cc3[VAR4_size];
for (i=0; i<VAR4_size; i++) {
ch = 0;
temp = (VAR4>>i*8) & 0x000000FF;
for (int j=0; j<8; j++) {
temp2 = temp & (1<<j);
if (temp2!=0) ch |= 1<<j;
}
cc3[VAR4_size-1-i] = ch;
}
ch = read_int(cc3, VAR4_size);
if (ch == 0x8) {
fputs("@CONDITION3:VAR4@$IMPLICIT_DATAFLOW2$##", fp);
//@NOISE@
fputs("\n", fp);
fclose(fp);
fp = NULL;
bug();
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION3:VAR4@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION1:VAR3@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION4:VAR2@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION2:VAR1@##", fp);
}

    //// section of insertion
    if (fp != NULL) {
        fputs("\n", fp);
        fclose(fp);
    }
}

//// section of main function
