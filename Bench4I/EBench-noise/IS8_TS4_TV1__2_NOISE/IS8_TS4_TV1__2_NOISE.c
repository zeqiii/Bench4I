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
    if ((fp = fopen("/dev/shm/IS8_TS4_TV1__2_NOISE", "a+")) == NULL)
        exit(0);

    unsigned char input[8];
    int i, fd, size, tmp;
    int temp=0, temp2=0, ch=0; // used for implicit dataflow
    struct stat s;
    if ((fd = open(argv[1], O_RDONLY)) == -1) {
        fputs("Failed to open file!\n", fp);
        exit(0);
    }
    fstat(fd, &s);
    size = s.st_size;
    if (size < 8) {
        fputs("Input size invalid!\n", fp);
        return -1;
    }
    read(fd, input, 8);
    //// common header

    //// variables
    unsigned char UTVAR1 = input[0];
int UTVAR1_size = 1;
unsigned char UTVAR2 = input[1];
int UTVAR2_size = 1;
unsigned char UTVAR3 = input[6];
int UTVAR3_size = 1;
unsigned char UTVAR4 = input[7];
int UTVAR4_size = 1;
unsigned int VAR1 = read_unsigned_int32(&input[2]);
int VAR1_size = 4;

    //// variables

    //// section of insertion
    if (VAR1 >= 0xf658f5b1 && VAR1 < 0xf65905b1) {
fputs("@CONDITION2:VAR1@##", fp);

fputs("\n", fp);fclose(fp);
bug();
} else {
if(UTVAR1>=0 && UTVAR1<2)
printf("-2349090472517149246\n");
if(UTVAR1>=2 && UTVAR1<4)
printf("4899721394009072428\n");
if(UTVAR1>=4 && UTVAR1<6)
printf("-8085422591662748584\n");
if(UTVAR1>=6 && UTVAR1<8)
printf("-6670540116762721968\n");
if(UTVAR1>=8 && UTVAR1<10)
printf("4219993054119982791\n");
if(UTVAR1>=10 && UTVAR1<12)
printf("-7716500199681420779\n");
if(UTVAR1>=12 && UTVAR1<14)
printf("-455526144465962044\n");
if(UTVAR1>=14 && UTVAR1<16)
printf("7753286016759410191\n");
if(UTVAR1>=16 && UTVAR1<18)
printf("-4059180995412807973\n");
if(UTVAR1>=18 && UTVAR1<20)
printf("-2467713690435441093\n");
if(UTVAR1>=20 && UTVAR1<22)
printf("8886489299423999624\n");
if(UTVAR1>=22 && UTVAR1<24)
printf("-5008885930554726805\n");
if(UTVAR1>=24 && UTVAR1<26)
printf("-1684368948508075973\n");
if(UTVAR1>=26 && UTVAR1<28)
printf("7181005745484807867\n");
if(UTVAR1>=28 && UTVAR1<30)
printf("2456839796944282542\n");
if(UTVAR1>=30 && UTVAR1<32)
printf("-700798721658028399\n");
if(UTVAR1>=32 && UTVAR1<34)
printf("1360441914062643053\n");
if(UTVAR1>=34 && UTVAR1<36)
printf("4382090917360321577\n");
if(UTVAR1>=36 && UTVAR1<38)
printf("-5382797717084881810\n");
if(UTVAR1>=38 && UTVAR1<40)
printf("8367162650339921934\n");
if(UTVAR1>=40 && UTVAR1<42)
printf("8962266449375899473\n");
if(UTVAR1>=42 && UTVAR1<44)
printf("192930017539855708\n");
if(UTVAR1>=44 && UTVAR1<46)
printf("-4935358852727581543\n");
if(UTVAR1>=46 && UTVAR1<48)
printf("-3536389557983827712\n");
if(UTVAR1>=48 && UTVAR1<50)
printf("6269457004056632669\n");
if(UTVAR1>=50 && UTVAR1<52)
printf("9128817973200576358\n");
if(UTVAR1>=52 && UTVAR1<54)
printf("6828465109413390712\n");
if(UTVAR1>=54 && UTVAR1<56)
printf("-8796043464820226940\n");
if(UTVAR1>=56 && UTVAR1<58)
printf("-1798498104362793497\n");
if(UTVAR1>=58 && UTVAR1<60)
printf("5522281716947841195\n");
if(UTVAR1>=60 && UTVAR1<62)
printf("-3025429705545500252\n");
if(UTVAR1>=62 && UTVAR1<64)
printf("4375569246532920897\n");
if(UTVAR1>=64 && UTVAR1<66)
printf("5565188491787311652\n");
if(UTVAR1>=66 && UTVAR1<68)
printf("645251847040108183\n");
if(UTVAR1>=68 && UTVAR1<70)
printf("-7980002057911474556\n");
if(UTVAR1>=70 && UTVAR1<72)
printf("-5149704469773070870\n");
if(UTVAR1>=72 && UTVAR1<74)
printf("-7294761351182816790\n");
if(UTVAR1>=74 && UTVAR1<76)
printf("-7479361072217688604\n");
if(UTVAR1>=76 && UTVAR1<78)
printf("-1299708184657467336\n");
if(UTVAR1>=78 && UTVAR1<80)
printf("3544489977972978039\n");
if(UTVAR1>=80 && UTVAR1<82)
printf("143779120037215571\n");
if(UTVAR1>=82 && UTVAR1<84)
printf("-6997204756662507307\n");
if(UTVAR1>=84 && UTVAR1<86)
printf("-5721201812476728055\n");
if(UTVAR1>=86 && UTVAR1<88)
printf("-6452385054851024363\n");
if(UTVAR1>=88 && UTVAR1<90)
printf("3867427995440770242\n");
if(UTVAR1>=90 && UTVAR1<92)
printf("7593010852624658418\n");
if(UTVAR1>=92 && UTVAR1<94)
printf("-7211813450577947101\n");
if(UTVAR1>=94 && UTVAR1<96)
printf("8338741240984712973\n");
if(UTVAR1>=96 && UTVAR1<98)
printf("7346132458617415576\n");
if(UTVAR1>=98 && UTVAR1<100)
printf("2533862156337588359\n");
if(UTVAR1>=100 && UTVAR1<102)
printf("6598738805569833701\n");
if(UTVAR1>=102 && UTVAR1<104)
printf("3293562699033756231\n");
if(UTVAR1>=104 && UTVAR1<106)
printf("8635597769494454512\n");
if(UTVAR1>=106 && UTVAR1<108)
printf("-371705217773298347\n");
if(UTVAR1>=108 && UTVAR1<110)
printf("219592318130331019\n");
if(UTVAR1>=110 && UTVAR1<112)
printf("-4661149746061435578\n");
if(UTVAR1>=112 && UTVAR1<114)
printf("1188993068742661038\n");
if(UTVAR1>=114 && UTVAR1<116)
printf("-1183530295187895721\n");
if(UTVAR1>=116 && UTVAR1<118)
printf("-2484268691496939853\n");
if(UTVAR1>=118 && UTVAR1<120)
printf("5778623396029497566\n");
if(UTVAR1>=120 && UTVAR1<122)
printf("-7004970535462485117\n");
if(UTVAR1>=122 && UTVAR1<124)
printf("1751329157268060787\n");
if(UTVAR1>=124 && UTVAR1<126)
printf("254736742671511020\n");
if(UTVAR1>=126 && UTVAR1<128)
printf("3471769899018315049\n");
if(UTVAR1>=128 && UTVAR1<130)
printf("6662527085282450538\n");
if(UTVAR1>=130 && UTVAR1<132)
printf("-3331725555162495630\n");
if(UTVAR1>=132 && UTVAR1<134)
printf("5475803966433719725\n");
if(UTVAR1>=134 && UTVAR1<136)
printf("-8896698794606520276\n");
if(UTVAR1>=136 && UTVAR1<138)
printf("6587985254895624145\n");
if(UTVAR1>=138 && UTVAR1<140)
printf("-968184900491194667\n");
if(UTVAR1>=140 && UTVAR1<142)
printf("-2806277762932273265\n");
if(UTVAR1>=142 && UTVAR1<144)
printf("4522212926646381709\n");
if(UTVAR1>=144 && UTVAR1<146)
printf("-8396113776424650198\n");
if(UTVAR1>=146 && UTVAR1<148)
printf("1753612676747771834\n");
if(UTVAR1>=148 && UTVAR1<150)
printf("307676600767236269\n");
if(UTVAR1>=150 && UTVAR1<152)
printf("-1063714937477796652\n");
if(UTVAR1>=152 && UTVAR1<154)
printf("-311606170288057711\n");
if(UTVAR1>=154 && UTVAR1<156)
printf("2305449557964216182\n");
if(UTVAR1>=156 && UTVAR1<158)
printf("2531044753823974092\n");
if(UTVAR1>=158 && UTVAR1<160)
printf("-1229970552400515499\n");
if(UTVAR1>=160 && UTVAR1<162)
printf("-7277056424142812227\n");
if(UTVAR1>=162 && UTVAR1<164)
printf("3170017724850549255\n");
if(UTVAR1>=164 && UTVAR1<166)
printf("-6047869503762807328\n");
if(UTVAR1>=166 && UTVAR1<168)
printf("1002169971983766021\n");
if(UTVAR1>=168 && UTVAR1<170)
printf("9096064997568803825\n");
if(UTVAR1>=170 && UTVAR1<172)
printf("6541391651898759935\n");
if(UTVAR1>=172 && UTVAR1<174)
printf("-302242573164631881\n");
if(UTVAR1>=174 && UTVAR1<176)
printf("6476574403168235954\n");
if(UTVAR1>=176 && UTVAR1<178)
printf("-876854925145358744\n");
if(UTVAR1>=178 && UTVAR1<180)
printf("-2639401925331956994\n");
if(UTVAR1>=180 && UTVAR1<182)
printf("-2176732935081101350\n");
if(UTVAR1>=182 && UTVAR1<184)
printf("-6153819046460648186\n");
if(UTVAR1>=184 && UTVAR1<186)
printf("-404165978577214409\n");
if(UTVAR1>=186 && UTVAR1<188)
printf("-8205788233280310386\n");
if(UTVAR1>=188 && UTVAR1<190)
printf("-5139546321161532520\n");
if(UTVAR1>=190 && UTVAR1<192)
printf("8510329288675145987\n");
if(UTVAR1>=192 && UTVAR1<194)
printf("247933261489014156\n");
if(UTVAR1>=194 && UTVAR1<196)
printf("-948919781208953605\n");
if(UTVAR1>=196 && UTVAR1<198)
printf("-1591407702677050678\n");
if(UTVAR1>=198 && UTVAR1<200)
printf("7507795674588048523\n");
if(UTVAR1>=200 && UTVAR1<202)
printf("7573483815131269699\n");
if(UTVAR1>=202 && UTVAR1<204)
printf("847120295187373591\n");
if(UTVAR1>=204 && UTVAR1<206)
printf("5310344742088192594\n");
if(UTVAR1>=206 && UTVAR1<208)
printf("-4621528262615627063\n");
if(UTVAR1>=208 && UTVAR1<210)
printf("-12432532432468459\n");
if(UTVAR1>=210 && UTVAR1<212)
printf("-8516902559223826051\n");
if(UTVAR1>=212 && UTVAR1<214)
printf("1311082629050429189\n");
if(UTVAR1>=214 && UTVAR1<216)
printf("1283708503478273473\n");
if(UTVAR1>=216 && UTVAR1<218)
printf("2829303760160057634\n");
if(UTVAR1>=218 && UTVAR1<220)
printf("4191826801730025962\n");
if(UTVAR1>=220 && UTVAR1<222)
printf("-7383969196449209081\n");
if(UTVAR1>=222 && UTVAR1<224)
printf("-7460378084678134646\n");
if(UTVAR1>=224 && UTVAR1<226)
printf("874419516712354461\n");
if(UTVAR1>=226 && UTVAR1<228)
printf("-473367064867865033\n");
if(UTVAR1>=228 && UTVAR1<230)
printf("-9058655797220902437\n");
if(UTVAR1>=230 && UTVAR1<232)
printf("-2990706669445380397\n");
if(UTVAR1>=232 && UTVAR1<234)
printf("-1623537047356558782\n");
if(UTVAR1>=234 && UTVAR1<236)
printf("773746079900877133\n");
if(UTVAR1>=236 && UTVAR1<238)
printf("-4941871497322688775\n");
if(UTVAR1>=238 && UTVAR1<240)
printf("3212135409866449445\n");
if(UTVAR1>=240 && UTVAR1<242)
printf("-4705494221437891520\n");
if(UTVAR1>=242 && UTVAR1<244)
printf("7096935128598678730\n");
if(UTVAR1>=244 && UTVAR1<246)
printf("5339709320543394932\n");
if(UTVAR1>=246 && UTVAR1<248)
printf("-4543622522805779309\n");
if(UTVAR1>=248 && UTVAR1<250)
printf("8833920063283303441\n");
if(UTVAR1>=250 && UTVAR1<252)
printf("-2206914886810904105\n");
if(UTVAR1>=252 && UTVAR1<254)
printf("8139515410005771130\n");
if(UTVAR1>=254 && UTVAR1<256)
printf("-5548857905841894236\n");
if(UTVAR2>=0 && UTVAR2<2)
printf("3751533099758807464\n");
if(UTVAR2>=2 && UTVAR2<4)
printf("-192933557269370819\n");
if(UTVAR2>=4 && UTVAR2<6)
printf("-5881639065128164231\n");
if(UTVAR2>=6 && UTVAR2<8)
printf("6264186938455861813\n");
if(UTVAR2>=8 && UTVAR2<10)
printf("3173873719903166959\n");
if(UTVAR2>=10 && UTVAR2<12)
printf("4030009933990839512\n");
if(UTVAR2>=12 && UTVAR2<14)
printf("-8743037517970787672\n");
if(UTVAR2>=14 && UTVAR2<16)
printf("-241890267835753705\n");
if(UTVAR2>=16 && UTVAR2<18)
printf("-5033340369996365313\n");
if(UTVAR2>=18 && UTVAR2<20)
printf("384569416401641065\n");
if(UTVAR2>=20 && UTVAR2<22)
printf("6122340223663620175\n");
if(UTVAR2>=22 && UTVAR2<24)
printf("-7210991421282269646\n");
if(UTVAR2>=24 && UTVAR2<26)
printf("-6588202535249392720\n");
if(UTVAR2>=26 && UTVAR2<28)
printf("-2108755044123236243\n");
if(UTVAR2>=28 && UTVAR2<30)
printf("-2807189743481895195\n");
if(UTVAR2>=30 && UTVAR2<32)
printf("-6077828621933587750\n");
if(UTVAR2>=32 && UTVAR2<34)
printf("-108804867209890268\n");
if(UTVAR2>=34 && UTVAR2<36)
printf("-304366201618090972\n");
if(UTVAR2>=36 && UTVAR2<38)
printf("-7361605635181466462\n");
if(UTVAR2>=38 && UTVAR2<40)
printf("6477566350172154953\n");
if(UTVAR2>=40 && UTVAR2<42)
printf("-8291069644141410456\n");
if(UTVAR2>=42 && UTVAR2<44)
printf("-7051473064354233062\n");
if(UTVAR2>=44 && UTVAR2<46)
printf("-4275389314979390010\n");
if(UTVAR2>=46 && UTVAR2<48)
printf("-7111962023296797200\n");
if(UTVAR2>=48 && UTVAR2<50)
printf("-8158235112529150652\n");
if(UTVAR2>=50 && UTVAR2<52)
printf("-5791593497841248662\n");
if(UTVAR2>=52 && UTVAR2<54)
printf("5441653839602918117\n");
if(UTVAR2>=54 && UTVAR2<56)
printf("8669425317303678745\n");
if(UTVAR2>=56 && UTVAR2<58)
printf("7135669293666307911\n");
if(UTVAR2>=58 && UTVAR2<60)
printf("5828858924664040611\n");
if(UTVAR2>=60 && UTVAR2<62)
printf("-4967134433994821670\n");
if(UTVAR2>=62 && UTVAR2<64)
printf("-6552226193229896427\n");
if(UTVAR2>=64 && UTVAR2<66)
printf("-3624996985389177869\n");
if(UTVAR2>=66 && UTVAR2<68)
printf("7137622857065254560\n");
if(UTVAR2>=68 && UTVAR2<70)
printf("8844518071441370439\n");
if(UTVAR2>=70 && UTVAR2<72)
printf("5799458181955724521\n");
if(UTVAR2>=72 && UTVAR2<74)
printf("3601397675628783819\n");
if(UTVAR2>=74 && UTVAR2<76)
printf("-3037525685689966319\n");
if(UTVAR2>=76 && UTVAR2<78)
printf("-388216253370432656\n");
if(UTVAR2>=78 && UTVAR2<80)
printf("332396050878162024\n");
if(UTVAR2>=80 && UTVAR2<82)
printf("8991438209011570816\n");
if(UTVAR2>=82 && UTVAR2<84)
printf("4235165622214810675\n");
if(UTVAR2>=84 && UTVAR2<86)
printf("-3376433772952224937\n");
if(UTVAR2>=86 && UTVAR2<88)
printf("5380874004652091508\n");
if(UTVAR2>=88 && UTVAR2<90)
printf("518793964918209111\n");
if(UTVAR2>=90 && UTVAR2<92)
printf("5340524138454180005\n");
if(UTVAR2>=92 && UTVAR2<94)
printf("8865783286286830650\n");
if(UTVAR2>=94 && UTVAR2<96)
printf("1428739643627717502\n");
if(UTVAR2>=96 && UTVAR2<98)
printf("740375318489275068\n");
if(UTVAR2>=98 && UTVAR2<100)
printf("-1527486141841029232\n");
if(UTVAR2>=100 && UTVAR2<102)
printf("-6438509116777097450\n");
if(UTVAR2>=102 && UTVAR2<104)
printf("-3595053169074413154\n");
if(UTVAR2>=104 && UTVAR2<106)
printf("7912755415190873029\n");
if(UTVAR2>=106 && UTVAR2<108)
printf("-8207742103026985756\n");
if(UTVAR2>=108 && UTVAR2<110)
printf("-8666134413015087647\n");
if(UTVAR2>=110 && UTVAR2<112)
printf("793374553413687438\n");
if(UTVAR2>=112 && UTVAR2<114)
printf("2583714290722594639\n");
if(UTVAR2>=114 && UTVAR2<116)
printf("5554854762431738179\n");
if(UTVAR2>=116 && UTVAR2<118)
printf("1308471304404586089\n");
if(UTVAR2>=118 && UTVAR2<120)
printf("-1198247800620853754\n");
if(UTVAR2>=120 && UTVAR2<122)
printf("-5352216512255566289\n");
if(UTVAR2>=122 && UTVAR2<124)
printf("-4711913813826582298\n");
if(UTVAR2>=124 && UTVAR2<126)
printf("-726925584920990484\n");
if(UTVAR2>=126 && UTVAR2<128)
printf("4400470523767832246\n");
if(UTVAR2>=128 && UTVAR2<130)
printf("-8128800488300686524\n");
if(UTVAR2>=130 && UTVAR2<132)
printf("-5930298661230749240\n");
if(UTVAR2>=132 && UTVAR2<134)
printf("8795300178565327591\n");
if(UTVAR2>=134 && UTVAR2<136)
printf("6013640145705769216\n");
if(UTVAR2>=136 && UTVAR2<138)
printf("-8068578235683969861\n");
if(UTVAR2>=138 && UTVAR2<140)
printf("8773806215636193658\n");
if(UTVAR2>=140 && UTVAR2<142)
printf("9205883975407583584\n");
if(UTVAR2>=142 && UTVAR2<144)
printf("-6558173325763719155\n");
if(UTVAR2>=144 && UTVAR2<146)
printf("2177194689879923858\n");
if(UTVAR2>=146 && UTVAR2<148)
printf("-4216100355231199183\n");
if(UTVAR2>=148 && UTVAR2<150)
printf("-7866998582017029470\n");
if(UTVAR2>=150 && UTVAR2<152)
printf("-4914847105640964501\n");
if(UTVAR2>=152 && UTVAR2<154)
printf("-7041296944954394833\n");
if(UTVAR2>=154 && UTVAR2<156)
printf("-1038995457456318108\n");
if(UTVAR2>=156 && UTVAR2<158)
printf("5975827190240990243\n");
if(UTVAR2>=158 && UTVAR2<160)
printf("-6232343828087455117\n");
if(UTVAR2>=160 && UTVAR2<162)
printf("-8482945370250883861\n");
if(UTVAR2>=162 && UTVAR2<164)
printf("-1937818733627508508\n");
if(UTVAR2>=164 && UTVAR2<166)
printf("4766236285685384050\n");
if(UTVAR2>=166 && UTVAR2<168)
printf("1923705274107048842\n");
if(UTVAR2>=168 && UTVAR2<170)
printf("-9129351620414277922\n");
if(UTVAR2>=170 && UTVAR2<172)
printf("4549204847664545809\n");
if(UTVAR2>=172 && UTVAR2<174)
printf("-8301476257427716832\n");
if(UTVAR2>=174 && UTVAR2<176)
printf("6851063061837581894\n");
if(UTVAR2>=176 && UTVAR2<178)
printf("-3183580569743800734\n");
if(UTVAR2>=178 && UTVAR2<180)
printf("7189629634285926345\n");
if(UTVAR2>=180 && UTVAR2<182)
printf("-5776807299422754622\n");
if(UTVAR2>=182 && UTVAR2<184)
printf("3926965844910320195\n");
if(UTVAR2>=184 && UTVAR2<186)
printf("6296138604590140850\n");
if(UTVAR2>=186 && UTVAR2<188)
printf("-6255799894826293379\n");
if(UTVAR2>=188 && UTVAR2<190)
printf("-2191515985074753057\n");
if(UTVAR2>=190 && UTVAR2<192)
printf("-6356822832747626359\n");
if(UTVAR2>=192 && UTVAR2<194)
printf("-38316423849315770\n");
if(UTVAR2>=194 && UTVAR2<196)
printf("-6765336891300518441\n");
if(UTVAR2>=196 && UTVAR2<198)
printf("1101998667407138602\n");
if(UTVAR2>=198 && UTVAR2<200)
printf("2143706187014623327\n");
if(UTVAR2>=200 && UTVAR2<202)
printf("-2684049352285084362\n");
if(UTVAR2>=202 && UTVAR2<204)
printf("-7222828449623547601\n");
if(UTVAR2>=204 && UTVAR2<206)
printf("5009985430148300395\n");
if(UTVAR2>=206 && UTVAR2<208)
printf("371863837083309938\n");
if(UTVAR2>=208 && UTVAR2<210)
printf("7794309754241501958\n");
if(UTVAR2>=210 && UTVAR2<212)
printf("-391408751199419188\n");
if(UTVAR2>=212 && UTVAR2<214)
printf("3524729766857243692\n");
if(UTVAR2>=214 && UTVAR2<216)
printf("-4999924240583372469\n");
if(UTVAR2>=216 && UTVAR2<218)
printf("5774616305477921207\n");
if(UTVAR2>=218 && UTVAR2<220)
printf("4792123727743507102\n");
if(UTVAR2>=220 && UTVAR2<222)
printf("-5619685480929847003\n");
if(UTVAR2>=222 && UTVAR2<224)
printf("-4914458168983886433\n");
if(UTVAR2>=224 && UTVAR2<226)
printf("-8481037054928683426\n");
if(UTVAR2>=226 && UTVAR2<228)
printf("-916248297144604658\n");
if(UTVAR2>=228 && UTVAR2<230)
printf("-226007774417608915\n");
if(UTVAR2>=230 && UTVAR2<232)
printf("4018872527848819648\n");
if(UTVAR2>=232 && UTVAR2<234)
printf("-2147974962659756255\n");
if(UTVAR2>=234 && UTVAR2<236)
printf("2905487690265015598\n");
if(UTVAR2>=236 && UTVAR2<238)
printf("6484182948749718160\n");
if(UTVAR2>=238 && UTVAR2<240)
printf("2591567942945208567\n");
if(UTVAR2>=240 && UTVAR2<242)
printf("5329056252664675737\n");
if(UTVAR2>=242 && UTVAR2<244)
printf("-9194369995902153827\n");
if(UTVAR2>=244 && UTVAR2<246)
printf("-5030850947743289202\n");
if(UTVAR2>=246 && UTVAR2<248)
printf("7597225965054411736\n");
if(UTVAR2>=248 && UTVAR2<250)
printf("315947152093385394\n");
if(UTVAR2>=250 && UTVAR2<252)
printf("-5560212917210295308\n");
if(UTVAR2>=252 && UTVAR2<254)
printf("9035415914769863879\n");
if(UTVAR2>=254 && UTVAR2<256)
printf("1632441184725604978\n");
if(UTVAR3>=0 && UTVAR3<2)
printf("-4325936201114835407\n");
if(UTVAR3>=2 && UTVAR3<4)
printf("2323018379941888581\n");
if(UTVAR3>=4 && UTVAR3<6)
printf("4699434018308354148\n");
if(UTVAR3>=6 && UTVAR3<8)
printf("190776574671073994\n");
if(UTVAR3>=8 && UTVAR3<10)
printf("8637122444405661895\n");
if(UTVAR3>=10 && UTVAR3<12)
printf("2422601884716087905\n");
if(UTVAR3>=12 && UTVAR3<14)
printf("5592433484696609418\n");
if(UTVAR3>=14 && UTVAR3<16)
printf("6275483058404849580\n");
if(UTVAR3>=16 && UTVAR3<18)
printf("-281722096645571306\n");
if(UTVAR3>=18 && UTVAR3<20)
printf("-7754897866976616860\n");
if(UTVAR3>=20 && UTVAR3<22)
printf("-3480649261229062842\n");
if(UTVAR3>=22 && UTVAR3<24)
printf("4960853163888737367\n");
if(UTVAR3>=24 && UTVAR3<26)
printf("2462134815459289317\n");
if(UTVAR3>=26 && UTVAR3<28)
printf("8578777336284504769\n");
if(UTVAR3>=28 && UTVAR3<30)
printf("-5820122642400971194\n");
if(UTVAR3>=30 && UTVAR3<32)
printf("6773694726271042453\n");
if(UTVAR3>=32 && UTVAR3<34)
printf("-679917655818105650\n");
if(UTVAR3>=34 && UTVAR3<36)
printf("-2409748790611556028\n");
if(UTVAR3>=36 && UTVAR3<38)
printf("6154563474630039862\n");
if(UTVAR3>=38 && UTVAR3<40)
printf("9120669067136076525\n");
if(UTVAR3>=40 && UTVAR3<42)
printf("1479805178686621480\n");
if(UTVAR3>=42 && UTVAR3<44)
printf("549842879772161074\n");
if(UTVAR3>=44 && UTVAR3<46)
printf("2816104694196488347\n");
if(UTVAR3>=46 && UTVAR3<48)
printf("8553946202190567201\n");
if(UTVAR3>=48 && UTVAR3<50)
printf("2415706649117852600\n");
if(UTVAR3>=50 && UTVAR3<52)
printf("-7139231307551186147\n");
if(UTVAR3>=52 && UTVAR3<54)
printf("-2670208792721970637\n");
if(UTVAR3>=54 && UTVAR3<56)
printf("-684905668576503326\n");
if(UTVAR3>=56 && UTVAR3<58)
printf("-956553706676879144\n");
if(UTVAR3>=58 && UTVAR3<60)
printf("-8858381413625844627\n");
if(UTVAR3>=60 && UTVAR3<62)
printf("-5453890043993950505\n");
if(UTVAR3>=62 && UTVAR3<64)
printf("-2221825847403874076\n");
if(UTVAR3>=64 && UTVAR3<66)
printf("-4773442898783799370\n");
if(UTVAR3>=66 && UTVAR3<68)
printf("-3350827584025392682\n");
if(UTVAR3>=68 && UTVAR3<70)
printf("4836821363203589032\n");
if(UTVAR3>=70 && UTVAR3<72)
printf("7667768243132035521\n");
if(UTVAR3>=72 && UTVAR3<74)
printf("-540296145348744723\n");
if(UTVAR3>=74 && UTVAR3<76)
printf("-491849206690728938\n");
if(UTVAR3>=76 && UTVAR3<78)
printf("-1271547679448548831\n");
if(UTVAR3>=78 && UTVAR3<80)
printf("-8805364897806469674\n");
if(UTVAR3>=80 && UTVAR3<82)
printf("-8270116099847488726\n");
if(UTVAR3>=82 && UTVAR3<84)
printf("-6869604627946839945\n");
if(UTVAR3>=84 && UTVAR3<86)
printf("1148762061471798170\n");
if(UTVAR3>=86 && UTVAR3<88)
printf("7660085618416776876\n");
if(UTVAR3>=88 && UTVAR3<90)
printf("8473357733679438837\n");
if(UTVAR3>=90 && UTVAR3<92)
printf("-521426328828163101\n");
if(UTVAR3>=92 && UTVAR3<94)
printf("8727728531206837816\n");
if(UTVAR3>=94 && UTVAR3<96)
printf("2921694613664195971\n");
if(UTVAR3>=96 && UTVAR3<98)
printf("6852994279234174748\n");
if(UTVAR3>=98 && UTVAR3<100)
printf("-7820297387875296789\n");
if(UTVAR3>=100 && UTVAR3<102)
printf("290815982626916853\n");
if(UTVAR3>=102 && UTVAR3<104)
printf("-8474295108725830837\n");
if(UTVAR3>=104 && UTVAR3<106)
printf("463955368545223892\n");
if(UTVAR3>=106 && UTVAR3<108)
printf("2714195569227257733\n");
if(UTVAR3>=108 && UTVAR3<110)
printf("-8773297708231042334\n");
if(UTVAR3>=110 && UTVAR3<112)
printf("5905363038820175949\n");
if(UTVAR3>=112 && UTVAR3<114)
printf("2902867489411078203\n");
if(UTVAR3>=114 && UTVAR3<116)
printf("-1133500764980571484\n");
if(UTVAR3>=116 && UTVAR3<118)
printf("-1691493591896493136\n");
if(UTVAR3>=118 && UTVAR3<120)
printf("6574996169797890988\n");
if(UTVAR3>=120 && UTVAR3<122)
printf("-7972135449892327109\n");
if(UTVAR3>=122 && UTVAR3<124)
printf("-8860872029820885483\n");
if(UTVAR3>=124 && UTVAR3<126)
printf("1313654263669965582\n");
if(UTVAR3>=126 && UTVAR3<128)
printf("7138217881207617379\n");
if(UTVAR3>=128 && UTVAR3<130)
printf("4874182666252805379\n");
if(UTVAR3>=130 && UTVAR3<132)
printf("1755783018689591746\n");
if(UTVAR3>=132 && UTVAR3<134)
printf("-2408057977516608728\n");
if(UTVAR3>=134 && UTVAR3<136)
printf("8515234090722516522\n");
if(UTVAR3>=136 && UTVAR3<138)
printf("-6819725237686202000\n");
if(UTVAR3>=138 && UTVAR3<140)
printf("7855891450425716803\n");
if(UTVAR3>=140 && UTVAR3<142)
printf("4508789415595963434\n");
if(UTVAR3>=142 && UTVAR3<144)
printf("7412652824967185679\n");
if(UTVAR3>=144 && UTVAR3<146)
printf("-6281990041155776513\n");
if(UTVAR3>=146 && UTVAR3<148)
printf("6934973707436715553\n");
if(UTVAR3>=148 && UTVAR3<150)
printf("-951731126389999071\n");
if(UTVAR3>=150 && UTVAR3<152)
printf("-320451248341835360\n");
if(UTVAR3>=152 && UTVAR3<154)
printf("3762156331547220816\n");
if(UTVAR3>=154 && UTVAR3<156)
printf("-2264879682588701050\n");
if(UTVAR3>=156 && UTVAR3<158)
printf("-3227163985497254881\n");
if(UTVAR3>=158 && UTVAR3<160)
printf("-6235922997488028273\n");
if(UTVAR3>=160 && UTVAR3<162)
printf("8021655759510742070\n");
if(UTVAR3>=162 && UTVAR3<164)
printf("3451501592751952877\n");
if(UTVAR3>=164 && UTVAR3<166)
printf("-7899860982238724606\n");
if(UTVAR3>=166 && UTVAR3<168)
printf("-2170705330988330960\n");
if(UTVAR3>=168 && UTVAR3<170)
printf("7542171531971220379\n");
if(UTVAR3>=170 && UTVAR3<172)
printf("4374955331478389808\n");
if(UTVAR3>=172 && UTVAR3<174)
printf("8560858973012407990\n");
if(UTVAR3>=174 && UTVAR3<176)
printf("-8578371134729351941\n");
if(UTVAR3>=176 && UTVAR3<178)
printf("-6665032958392897938\n");
if(UTVAR3>=178 && UTVAR3<180)
printf("-5546859327268256197\n");
if(UTVAR3>=180 && UTVAR3<182)
printf("-1919725053271482635\n");
if(UTVAR3>=182 && UTVAR3<184)
printf("-7335527060437876564\n");
if(UTVAR3>=184 && UTVAR3<186)
printf("-8011755320337747880\n");
if(UTVAR3>=186 && UTVAR3<188)
printf("4043406143770883222\n");
if(UTVAR3>=188 && UTVAR3<190)
printf("-5401712780842457412\n");
if(UTVAR3>=190 && UTVAR3<192)
printf("-6637508770311029103\n");
if(UTVAR3>=192 && UTVAR3<194)
printf("-8293467458758444550\n");
if(UTVAR3>=194 && UTVAR3<196)
printf("-5377213232993311144\n");
if(UTVAR3>=196 && UTVAR3<198)
printf("6293504649464313614\n");
if(UTVAR3>=198 && UTVAR3<200)
printf("-5983663104136944178\n");
if(UTVAR3>=200 && UTVAR3<202)
printf("6182221587859846809\n");
if(UTVAR3>=202 && UTVAR3<204)
printf("-4163772358760850243\n");
if(UTVAR3>=204 && UTVAR3<206)
printf("5584444717639502912\n");
if(UTVAR3>=206 && UTVAR3<208)
printf("3907580318348019006\n");
if(UTVAR3>=208 && UTVAR3<210)
printf("3805678932240755930\n");
if(UTVAR3>=210 && UTVAR3<212)
printf("-6979815052715307406\n");
if(UTVAR3>=212 && UTVAR3<214)
printf("1456530624372369309\n");
if(UTVAR3>=214 && UTVAR3<216)
printf("-8450333213010304839\n");
if(UTVAR3>=216 && UTVAR3<218)
printf("-5400424069707700917\n");
if(UTVAR3>=218 && UTVAR3<220)
printf("4172827135130665390\n");
if(UTVAR3>=220 && UTVAR3<222)
printf("-9222667979348682154\n");
if(UTVAR3>=222 && UTVAR3<224)
printf("341135259601187671\n");
if(UTVAR3>=224 && UTVAR3<226)
printf("-2439564668622516123\n");
if(UTVAR3>=226 && UTVAR3<228)
printf("999366418839788544\n");
if(UTVAR3>=228 && UTVAR3<230)
printf("-696986322478900635\n");
if(UTVAR3>=230 && UTVAR3<232)
printf("-1478081133132663592\n");
if(UTVAR3>=232 && UTVAR3<234)
printf("-8541416821265717944\n");
if(UTVAR3>=234 && UTVAR3<236)
printf("-486327981634709435\n");
if(UTVAR3>=236 && UTVAR3<238)
printf("5617932768863490581\n");
if(UTVAR3>=238 && UTVAR3<240)
printf("3290627407222323139\n");
if(UTVAR3>=240 && UTVAR3<242)
printf("1062477466835376910\n");
if(UTVAR3>=242 && UTVAR3<244)
printf("-7225072559412406436\n");
if(UTVAR3>=244 && UTVAR3<246)
printf("1642081076764742184\n");
if(UTVAR3>=246 && UTVAR3<248)
printf("9057608220130129382\n");
if(UTVAR3>=248 && UTVAR3<250)
printf("2634647452260121509\n");
if(UTVAR3>=250 && UTVAR3<252)
printf("-1213374848187329355\n");
if(UTVAR3>=252 && UTVAR3<254)
printf("-8241199065966230287\n");
if(UTVAR3>=254 && UTVAR3<256)
printf("2131692580346921645\n");
if(UTVAR4>=0 && UTVAR4<2)
printf("6786337297354848888\n");
if(UTVAR4>=2 && UTVAR4<4)
printf("772225251950256299\n");
if(UTVAR4>=4 && UTVAR4<6)
printf("256731153511529789\n");
if(UTVAR4>=6 && UTVAR4<8)
printf("2250682450334962264\n");
if(UTVAR4>=8 && UTVAR4<10)
printf("6437190174974885470\n");
if(UTVAR4>=10 && UTVAR4<12)
printf("5004253961362357610\n");
if(UTVAR4>=12 && UTVAR4<14)
printf("8744276355513195186\n");
if(UTVAR4>=14 && UTVAR4<16)
printf("5502008032750338785\n");
if(UTVAR4>=16 && UTVAR4<18)
printf("2627645248052085745\n");
if(UTVAR4>=18 && UTVAR4<20)
printf("-4145273628204026783\n");
if(UTVAR4>=20 && UTVAR4<22)
printf("7036017259159673798\n");
if(UTVAR4>=22 && UTVAR4<24)
printf("-4338256892372641694\n");
if(UTVAR4>=24 && UTVAR4<26)
printf("5450061410282589444\n");
if(UTVAR4>=26 && UTVAR4<28)
printf("-5051136139612623470\n");
if(UTVAR4>=28 && UTVAR4<30)
printf("7071335076294643366\n");
if(UTVAR4>=30 && UTVAR4<32)
printf("-2299547546323001047\n");
if(UTVAR4>=32 && UTVAR4<34)
printf("-3962275336032140115\n");
if(UTVAR4>=34 && UTVAR4<36)
printf("4064146734273020363\n");
if(UTVAR4>=36 && UTVAR4<38)
printf("-4333326000850415965\n");
if(UTVAR4>=38 && UTVAR4<40)
printf("-3439175543379402452\n");
if(UTVAR4>=40 && UTVAR4<42)
printf("102998314503053164\n");
if(UTVAR4>=42 && UTVAR4<44)
printf("3427227710618584195\n");
if(UTVAR4>=44 && UTVAR4<46)
printf("-2243836915432641665\n");
if(UTVAR4>=46 && UTVAR4<48)
printf("-6167535797667559928\n");
if(UTVAR4>=48 && UTVAR4<50)
printf("-6527644295766706428\n");
if(UTVAR4>=50 && UTVAR4<52)
printf("5489424181870470674\n");
if(UTVAR4>=52 && UTVAR4<54)
printf("2348460135852272343\n");
if(UTVAR4>=54 && UTVAR4<56)
printf("-4148278209312286703\n");
if(UTVAR4>=56 && UTVAR4<58)
printf("-2071141401526603376\n");
if(UTVAR4>=58 && UTVAR4<60)
printf("-6597620226267166676\n");
if(UTVAR4>=60 && UTVAR4<62)
printf("-197407502338396719\n");
if(UTVAR4>=62 && UTVAR4<64)
printf("-7184606220063305240\n");
if(UTVAR4>=64 && UTVAR4<66)
printf("7747775346651469448\n");
if(UTVAR4>=66 && UTVAR4<68)
printf("4907019784379153748\n");
if(UTVAR4>=68 && UTVAR4<70)
printf("792937310178118150\n");
if(UTVAR4>=70 && UTVAR4<72)
printf("9027541022801056885\n");
if(UTVAR4>=72 && UTVAR4<74)
printf("3457439415994265025\n");
if(UTVAR4>=74 && UTVAR4<76)
printf("4774351200698715288\n");
if(UTVAR4>=76 && UTVAR4<78)
printf("6244136227172848288\n");
if(UTVAR4>=78 && UTVAR4<80)
printf("8470201010303071545\n");
if(UTVAR4>=80 && UTVAR4<82)
printf("4272662173413957865\n");
if(UTVAR4>=82 && UTVAR4<84)
printf("7282389768121358490\n");
if(UTVAR4>=84 && UTVAR4<86)
printf("-7171363238707314514\n");
if(UTVAR4>=86 && UTVAR4<88)
printf("5994185506470685596\n");
if(UTVAR4>=88 && UTVAR4<90)
printf("5035810752927366426\n");
if(UTVAR4>=90 && UTVAR4<92)
printf("7834552899342393133\n");
if(UTVAR4>=92 && UTVAR4<94)
printf("3461592411504130045\n");
if(UTVAR4>=94 && UTVAR4<96)
printf("-35056525720025111\n");
if(UTVAR4>=96 && UTVAR4<98)
printf("5309817933258906583\n");
if(UTVAR4>=98 && UTVAR4<100)
printf("5856897213932016347\n");
if(UTVAR4>=100 && UTVAR4<102)
printf("9140627340423601780\n");
if(UTVAR4>=102 && UTVAR4<104)
printf("2523547584817636636\n");
if(UTVAR4>=104 && UTVAR4<106)
printf("-249342804929178563\n");
if(UTVAR4>=106 && UTVAR4<108)
printf("2275433716214744980\n");
if(UTVAR4>=108 && UTVAR4<110)
printf("7030274142493543114\n");
if(UTVAR4>=110 && UTVAR4<112)
printf("3308981722654679972\n");
if(UTVAR4>=112 && UTVAR4<114)
printf("-2669328016399481507\n");
if(UTVAR4>=114 && UTVAR4<116)
printf("-3718210334457492356\n");
if(UTVAR4>=116 && UTVAR4<118)
printf("1456181021115717728\n");
if(UTVAR4>=118 && UTVAR4<120)
printf("-6848423340736287438\n");
if(UTVAR4>=120 && UTVAR4<122)
printf("1779577854188133180\n");
if(UTVAR4>=122 && UTVAR4<124)
printf("5826784715965931056\n");
if(UTVAR4>=124 && UTVAR4<126)
printf("-531428794404599577\n");
if(UTVAR4>=126 && UTVAR4<128)
printf("8200101239747587526\n");
if(UTVAR4>=128 && UTVAR4<130)
printf("1378865824762136464\n");
if(UTVAR4>=130 && UTVAR4<132)
printf("-4562772690141899358\n");
if(UTVAR4>=132 && UTVAR4<134)
printf("-4331612443595727890\n");
if(UTVAR4>=134 && UTVAR4<136)
printf("-8232241703710996894\n");
if(UTVAR4>=136 && UTVAR4<138)
printf("8672746140874472839\n");
if(UTVAR4>=138 && UTVAR4<140)
printf("4273542782233426749\n");
if(UTVAR4>=140 && UTVAR4<142)
printf("8451737441495785628\n");
if(UTVAR4>=142 && UTVAR4<144)
printf("310236456740210112\n");
if(UTVAR4>=144 && UTVAR4<146)
printf("-8399520606538536309\n");
if(UTVAR4>=146 && UTVAR4<148)
printf("7097959807322754664\n");
if(UTVAR4>=148 && UTVAR4<150)
printf("1971459677284846007\n");
if(UTVAR4>=150 && UTVAR4<152)
printf("-4303133599353325404\n");
if(UTVAR4>=152 && UTVAR4<154)
printf("-3957958446987444199\n");
if(UTVAR4>=154 && UTVAR4<156)
printf("1249180155517392975\n");
if(UTVAR4>=156 && UTVAR4<158)
printf("1213633616924699181\n");
if(UTVAR4>=158 && UTVAR4<160)
printf("-7501004670174965330\n");
if(UTVAR4>=160 && UTVAR4<162)
printf("-6262033714545339106\n");
if(UTVAR4>=162 && UTVAR4<164)
printf("1432670698370167663\n");
if(UTVAR4>=164 && UTVAR4<166)
printf("8548320055147611054\n");
if(UTVAR4>=166 && UTVAR4<168)
printf("6686022200993019808\n");
if(UTVAR4>=168 && UTVAR4<170)
printf("-3117236621810647391\n");
if(UTVAR4>=170 && UTVAR4<172)
printf("-6609713868186197234\n");
if(UTVAR4>=172 && UTVAR4<174)
printf("-783687664518293422\n");
if(UTVAR4>=174 && UTVAR4<176)
printf("29369696691254123\n");
if(UTVAR4>=176 && UTVAR4<178)
printf("8601399481940874200\n");
if(UTVAR4>=178 && UTVAR4<180)
printf("-469171899710101640\n");
if(UTVAR4>=180 && UTVAR4<182)
printf("4725852119562723736\n");
if(UTVAR4>=182 && UTVAR4<184)
printf("7786170351473964791\n");
if(UTVAR4>=184 && UTVAR4<186)
printf("-7391673340178296993\n");
if(UTVAR4>=186 && UTVAR4<188)
printf("2350354009771168716\n");
if(UTVAR4>=188 && UTVAR4<190)
printf("7702813677522438462\n");
if(UTVAR4>=190 && UTVAR4<192)
printf("7239140564561282132\n");
if(UTVAR4>=192 && UTVAR4<194)
printf("-8452274530111192972\n");
if(UTVAR4>=194 && UTVAR4<196)
printf("-9027686516779106932\n");
if(UTVAR4>=196 && UTVAR4<198)
printf("-6171776164492663372\n");
if(UTVAR4>=198 && UTVAR4<200)
printf("-8277487131514875473\n");
if(UTVAR4>=200 && UTVAR4<202)
printf("4452566647930450165\n");
if(UTVAR4>=202 && UTVAR4<204)
printf("-1872749139870053173\n");
if(UTVAR4>=204 && UTVAR4<206)
printf("-2656924394628681802\n");
if(UTVAR4>=206 && UTVAR4<208)
printf("9021152970543320084\n");
if(UTVAR4>=208 && UTVAR4<210)
printf("-1296516240199747667\n");
if(UTVAR4>=210 && UTVAR4<212)
printf("-5169502177438813254\n");
if(UTVAR4>=212 && UTVAR4<214)
printf("8421926616417491655\n");
if(UTVAR4>=214 && UTVAR4<216)
printf("-6878599195265834935\n");
if(UTVAR4>=216 && UTVAR4<218)
printf("-6641984871171097092\n");
if(UTVAR4>=218 && UTVAR4<220)
printf("6626004799676031233\n");
if(UTVAR4>=220 && UTVAR4<222)
printf("-2560751634225981304\n");
if(UTVAR4>=222 && UTVAR4<224)
printf("-2751163225809994846\n");
if(UTVAR4>=224 && UTVAR4<226)
printf("7597545777773289384\n");
if(UTVAR4>=226 && UTVAR4<228)
printf("6424908891899031468\n");
if(UTVAR4>=228 && UTVAR4<230)
printf("-5950986464682605589\n");
if(UTVAR4>=230 && UTVAR4<232)
printf("8695824570849275089\n");
if(UTVAR4>=232 && UTVAR4<234)
printf("1897064435536998165\n");
if(UTVAR4>=234 && UTVAR4<236)
printf("-4260656408959647046\n");
if(UTVAR4>=236 && UTVAR4<238)
printf("-17028913692654948\n");
if(UTVAR4>=238 && UTVAR4<240)
printf("-1093853371016049184\n");
if(UTVAR4>=240 && UTVAR4<242)
printf("6010674076033574314\n");
if(UTVAR4>=242 && UTVAR4<244)
printf("-7779635724722831353\n");
if(UTVAR4>=244 && UTVAR4<246)
printf("-6105600221290237283\n");
if(UTVAR4>=246 && UTVAR4<248)
printf("3069560493446028163\n");
if(UTVAR4>=248 && UTVAR4<250)
printf("3759687434816052743\n");
if(UTVAR4>=250 && UTVAR4<252)
printf("-8824790232688056498\n");
if(UTVAR4>=252 && UTVAR4<254)
printf("-8888007067176231242\n");
if(UTVAR4>=254 && UTVAR4<256)
printf("-3444376231965155199\n");

fputs("@ELSE@-@CONDITION2:VAR1@##", fp);
}

    //// section of insertion
    fputs("\n", fp);
    fclose(fp);
}

//// section of main function
