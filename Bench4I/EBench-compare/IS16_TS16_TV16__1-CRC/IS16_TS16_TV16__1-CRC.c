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
    if ((fp = fopen("/dev/shm/IS16_TS16_TV16__1-CRC", "a+")) == NULL)
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
    unsigned char VAR10 = input[9];
int VAR10_size = 1;
unsigned char VAR11 = input[10];
int VAR11_size = 1;
unsigned char VAR12 = input[11];
int VAR12_size = 1;
unsigned char VAR13 = input[12];
int VAR13_size = 1;
unsigned char VAR14 = input[13];
int VAR14_size = 1;
unsigned char VAR15 = input[14];
int VAR15_size = 1;
unsigned char VAR16 = input[15];
int VAR16_size = 1;
unsigned char VAR1 = input[0];
int VAR1_size = 1;
unsigned char VAR2 = input[1];
int VAR2_size = 1;
unsigned char VAR3 = input[2];
int VAR3_size = 1;
unsigned char VAR4 = input[3];
int VAR4_size = 1;
unsigned char VAR5 = input[4];
int VAR5_size = 1;
unsigned char VAR6 = input[5];
int VAR6_size = 1;
unsigned char VAR7 = input[6];
int VAR7_size = 1;
unsigned char VAR8 = input[7];
int VAR8_size = 1;
unsigned char VAR9 = input[8];
int VAR9_size = 1;

    //// variables

    //// section of insertion
    unsigned char* tmp0 = int2byte(VAR13, VAR13_size);
if (crc(tmp0, VAR13_size) == 56781) {
fputs("@CONDITION10:VAR13@$CRC$##", fp);
//@NOISE@
unsigned char* tmp1 = int2byte(VAR8, VAR8_size);
if (crc(tmp1, VAR8_size) == 23749) {
fputs("@CONDITION15:VAR8@$CRC$##", fp);
//@NOISE@
unsigned char* tmp2 = int2byte(VAR9, VAR9_size);
if (crc(tmp2, VAR9_size) == 26358) {
fputs("@CONDITION16:VAR9@$CRC$##", fp);
//@NOISE@
unsigned char* tmp3 = int2byte(VAR14, VAR14_size);
if (crc(tmp3, VAR14_size) == 52716) {
fputs("@CONDITION14:VAR14@$CRC$##", fp);
//@NOISE@
unsigned char* tmp4 = int2byte(VAR15, VAR15_size);
if (crc(tmp4, VAR15_size) == 46939) {
fputs("@CONDITION12:VAR15@$CRC$##", fp);
//@NOISE@
unsigned char* tmp5 = int2byte(VAR7, VAR7_size);
if (crc(tmp5, VAR7_size) == 48923) {
fputs("@CONDITION9:VAR7@$CRC$##", fp);
//@NOISE@
unsigned char* tmp6 = int2byte(VAR10, VAR10_size);
if (crc(tmp6, VAR10_size) == 15363) {
fputs("@CONDITION11:VAR10@$CRC$##", fp);
//@NOISE@
unsigned char* tmp7 = int2byte(VAR11, VAR11_size);
if (crc(tmp7, VAR11_size) == 29895) {
fputs("@CONDITION13:VAR11@$CRC$##", fp);
//@NOISE@
unsigned char* tmp8 = int2byte(VAR12, VAR12_size);
if (crc(tmp8, VAR12_size) == 7761) {
fputs("@CONDITION7:VAR12@$CRC$##", fp);
//@NOISE@
unsigned char* tmp9 = int2byte(VAR2, VAR2_size);
if (crc(tmp9, VAR2_size) == 56781) {
fputs("@CONDITION6:VAR2@$CRC$##", fp);
//@NOISE@
unsigned char* tmp10 = int2byte(VAR4, VAR4_size);
if (crc(tmp10, VAR4_size) == 63455) {
fputs("@CONDITION4:VAR4@$CRC$##", fp);
//@NOISE@
unsigned char* tmp11 = int2byte(VAR5, VAR5_size);
if (crc(tmp11, VAR5_size) == 12915) {
fputs("@CONDITION5:VAR5@$CRC$##", fp);
//@NOISE@
unsigned char* tmp12 = int2byte(VAR1, VAR1_size);
if (crc(tmp12, VAR1_size) == 27286) {
fputs("@CONDITION3:VAR1@$CRC$##", fp);
//@NOISE@
unsigned char* tmp13 = int2byte(VAR16, VAR16_size);
if (crc(tmp13, VAR16_size) == 55197) {
fputs("@CONDITION2:VAR16@$CRC$##", fp);
//@NOISE@
unsigned char* tmp14 = int2byte(VAR14, VAR14_size);
if (crc(tmp14, VAR14_size) == 52716) {
fputs("@CONDITION14:VAR14@$CRC$##", fp);
//@NOISE@
unsigned char* tmp15 = int2byte(VAR6, VAR6_size);
if (crc(tmp15, VAR6_size) == 8786) {
fputs("@CONDITION8:VAR6@$CRC$##", fp);
//@NOISE@
fputs("\n", fp);
fclose(fp);
fp = NULL;
bug();
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION8:VAR6@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION14:VAR14@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION2:VAR16@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION3:VAR1@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION5:VAR5@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION4:VAR4@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION6:VAR2@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION7:VAR12@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION13:VAR11@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION11:VAR10@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION9:VAR7@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION12:VAR15@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION14:VAR14@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION16:VAR9@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION15:VAR8@##", fp);
}
} else {
//@NOISE@
fputs("@ELSE@-@CONDITION10:VAR13@##", fp);
}

    //// section of insertion
    if (fp != NULL) {
        fputs("\n", fp);
        fclose(fp);
    }
}

//// section of main function
