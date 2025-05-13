#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // int seed = time(0);
    int seed = 1819339300;
    printf("starting seed: %d\n", seed);
    // int target = 1943927208; 
    int target = 1355704377; 
    while (seed != 0 && seed < 2147483647) {
        srandom(seed);
        if (random() != 1943927208){
            seed++;
            continue;
        }
        if (random() == target) {
            printf("seed: %d\n", seed);
        }
        seed++;
    }
}