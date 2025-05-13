#include "crapto1.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>

uint32_t nums[6] = {2079876742, 4004465805, 2153128322, 205240755, 3206160223, 356672210};
int main(){
    uint64_t lfsr = 0xddb911cfa4a5;
    struct Crypto1State *s = crypto1_create(lfsr);
    uint32_t ks0 = crypto1_word(s, nums[0], 0);

    uint32_t ks1 = crypto1_word(s, nums[1], 1);
    uint32_t nr = nums[1] ^ ks1;
    uint32_t ks2 = crypto1_word(s, 0, 0);
    uint32_t ar = nums[2] ^ ks2;
    printf("ks0: %x\n", ks0);
    printf("ks1: %x\n", ks1);
    printf("nr: %x\n", nr);
    printf("ks2: %x\n", ks2);
    printf("ar: %x\n", ar);

    // struct Crypto1State *s2 = crypto1_create(lfsr);
    // crypto1_word(s2, nums[0], 0);

    // uint32_t nr = nums[1];
    // uint32_t ks1 = crypto1_word(s2, nr, 0);
    // printf("ks1: %x\n", ks1);

    // uint32_t nr_enc = nr ^ ks1;

    // uint32_t ks2 = crypto1_word(s2, 0, 0);
    // printf("ks2: %x\n", ks2);

    // uint32_t ar0_x = nums[2] ^ ks2;
    // printf("ar_x: %x\n", ar0_x);


    // // other one
    // s = crypto1_create(lfsr);
    // uint32_t ks0_2 = crypto1_word(s, nums[3], 0);
    // s2 = crypto1_create(lfsr);
    // nr = nums[4];
    // ks1 = crypto1_word(s2, nr, 0);
    // printf("ks1: %x\n", ks1);
    // nr_enc = nr ^ ks1;
    // ks2 = crypto1_word(s2, 0, 0);
    // printf("ks2: %x\n", ks2);
    // uint32_t ar0_x_2 = nums[5] ^ ks2;
    // printf("ar_x: %x\n", ar0_x_2);

//     uint32_t _ks1 = crypto1_word(s, nr_enc, 1);
//     printf("_ks1: %x\n", _ks1);

//     nr = nr_enc ^ _ks1;
//     uint32_t _ks2 = crypto1_word(s, 0, 0);
//     printf("_ks2: %x\n", _ks2);
}