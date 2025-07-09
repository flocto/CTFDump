#define _GNU_SOURCE
#include <curses.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define LOG_FILE "log.txt"

// Function pointer to the original srand
static void (*original_srand)(unsigned int seed) = NULL;

// Override srand function
void srand(unsigned int seed) {
    // Get the original srand function if not already loaded
    if (!original_srand) {
        original_srand = (void (*)(unsigned int))dlsym(RTLD_NEXT, "srand");
    }

    // Log the srand call
    FILE *log_file = fopen(LOG_FILE, "a");
    if (log_file) {
        time_t current_time = time(NULL);
        fprintf(log_file, "srand(%u) called at %s", seed, ctime(&current_time));
        fclose(log_file);
    }

    // Call the original srand function
    if (original_srand) {
        original_srand(seed);
    }
}

static WINDOW *(*original_initscr)(void) = NULL;

// Override initscr function
WINDOW *initscr(void) {
    // Get the original initscr function if not already loaded
    if (!original_initscr) {
        original_initscr = (WINDOW * (*)(void)) dlsym(RTLD_NEXT, "initscr");
    }

    // Log the initscr call
    FILE *log_file = fopen(LOG_FILE, "a");
    if (log_file) {
        time_t current_time = time(NULL);
        fprintf(log_file, "initscr() called at %s", ctime(&current_time));
        fclose(log_file);
    }

    // Grab regs
    uint64_t rsp, rbp;
    asm volatile("mov %%rsp, %0" : "=r"(rsp));
    asm volatile("mov %%rbp, %0" : "=r"(rbp));

    // Fetch last function rbp off stack
    uint64_t stored_rbp = *(uint64_t *)rbp;
    
    char* maze = (char*) (stored_rbp - 0x6760  );

    // Log vars
    log_file = fopen(LOG_FILE, "a");
    if (log_file) {
        fprintf(log_file, "Stack pointer (rsp): %llx\n", (unsigned long long)rsp);
        fprintf(log_file, "Base pointer (rbp): %llx\n", (unsigned long long)rbp);
        fprintf(log_file, "Stored base pointer (last function rbp): %llx\n", (unsigned long long)stored_rbp);
        fprintf(log_file, "Maze pointer: %p\n", maze);
        for (int i = 0; i < 21; i++) {
            for (int j = 0; j < 51; j++){
                fprintf(log_file, "%c", maze[i * 51 + j]);
            }
            fprintf(log_file, "\n");
        }
        fclose(log_file);
    }


    // Call the original initscr function
    if (original_initscr) {
        return original_initscr();
    }
    return NULL;  // Return NULL if original function is not found
}

/*
 * Compilation and usage instructions:
 *
 * To compile this file into a shared object (.so):
 * gcc -shared -fPIC -o preload.so preload.c -ldl
 *
 * To use the preload library:
 * LD_PRELOAD=./preload.so ./your_program
 *
 * Example:
 * LD_PRELOAD=./preload.so ls
 *
 * This will intercept all srand() calls made by the target program
 * and log them to "srand_log.txt" in the current directory.
 */