#include <stdio.h>

unsigned char *xxtea(unsigned char *key, unsigned char *v, int n) {
    unsigned int z = v[n - 1]; // last element of v
    unsigned int sum = 0x9E3779B9 * (52 / n) - 0x4AB325AA; // sum initialization
    unsigned int rounds = 0;
    unsigned int y, p;

    // loop until sum equals original sum value
    do {
        rounds -= 0x61C88647; // equivalent to adding delta (0x9E3779B9)
        unsigned int e = (rounds >> 2) & 0xF; // key index for this round

        // main loop to process all but the last element
        for (p = 0; p < n - 1; p++) {
            y = v[p + 1];
            v[p] += ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(p ^ e) & 0xF] ^ z));
            z = v[p];
        }

        // process the last element (wrap-around)
        y = v[0];
        v[n - 1] += ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(p ^ e) & 0xF] ^ z));
        z = v[n - 1];
        
    } while (rounds != sum);

    return v; 
}

char *xxtea_decrypt(char *key, char *v, int n) {
    unsigned int z = v[n - 1]; // last element of v
    unsigned int sum = 0x9E3779B9 * (52 / n) - 0x4AB325AA; // sum initialization (same as encryption)
    unsigned int rounds = sum;  // Start at the final sum value
    unsigned int y, p;

    // loop until rounds equals zero (reverse process)
    do {
        unsigned int e = (rounds >> 2) & 0xF; // key index for this round

        // process the last element (wrap-around)
        y = v[0];
        v[n - 1] -= ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(n - 1 ^ e) & 0xF] ^ z));
        z = v[n - 1];

        // main loop to process all but the last element
        for (p = n - 2; p >= 0; p--) {
            y = v[p + 1];
            v[p] -= ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(p ^ e) & 0xF] ^ z));
            z = v[p];
        }

        rounds += 0x61C88647; // equivalent to subtracting delta (reverse of encryption)

    } while (rounds != 0);

    return v; // return the decrypted data
}

int main() {
    unsigned char key[16] = "abcd1234ABCD1234";
    unsigned char v[28] = "hello this is sample messag\x01";
    unsigned char *result = xxtea(key, v, 28);

    printf("Encrypted: ");
    for (int i = 0; i < 28; i++) {
        printf("%02x", result[i]);
    }
    printf("\n");

    char *decrypted = xxtea_decrypt(key, v, 28);
    printf("Decrypted: %s\n", decrypted);
    return 0;
}