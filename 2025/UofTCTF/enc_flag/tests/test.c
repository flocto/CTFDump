#include <stdio.h>
#include <stdlib.h>

int main() {
    srandom(1);
    int i;
    for (i = 0; i < 10; i++) {
        printf("%ld\n", random());
    }
}