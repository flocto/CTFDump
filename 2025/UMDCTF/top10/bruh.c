#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main() {
    float fs[4] = {
        1.7268289323825639e+28, 1.726934359214294e+28, 1.0539650989449367e+24, 3.6204573916620575e-07
    };

    float a, b, c, d;
    a = fs[0];
    b = fs[1];
    c = fs[2];
    d = fs[3];

    float f0, f1, f2, f3;

    float prod = 5953314357248.0;

    //  a = f2 - f1
    //  b = f1 + f0
    //  c = f0 - f2

    //  a + b + c = 2 * f0
    f0 = (a + b + c) / 2;
    //  b = f1 + f0
    // f1 = b - f0
    f1 = b - f0;
    //  c = f0 - f2
    // f2 = f0 - c
    f2 = f0 - c;

    f3 = d / 2;

    f1 = prod / f3;

    printf("%lx\n", *(uint32_t *)&f0);
    printf("%lx\n", *(uint32_t *)&f1);
    printf("%lx\n", *(uint32_t *)&f2);
    printf("%lx\n", *(uint32_t *)&f3);

    printf("%.*s", 4, (char *)&f0);
    printf("%.*s", 4, (char *)&f1);
    printf("%.*s", 4, (char *)&f2);
    printf("%.*s", 4, (char *)&f3);
    printf("\n");
}