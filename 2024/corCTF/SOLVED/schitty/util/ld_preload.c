#define _GNU_SOURCE
#include <stdio.h>     // printf
#include <string.h>    // strcmp
#include <sys/stat.h>  // statf
#include <dlfcn.h>

int stat(const char *__restrict__ __file, struct stat *__restrict__ __buf) {
    int (*real_stat)(const char *__restrict__ __file, struct stat *__restrict__ __buf) = dlsym(RTLD_NEXT, "stat");
    if (strcmp(__file, "/bin/sh") == 0) {
        __buf->st_ino = 42467530;
        __buf->st_dev = 2050;
        __buf->st_rdev = 0;
        __buf->st_uid = 0;
        __buf->st_gid = 0;
        __buf->st_size = 125688;
        __buf->st_mtime = 1648043363;
        __buf->st_ctime = 1686442713;
        printf("stat: %s\n", __file);
        return 0;
    }
    return real_stat(__file, __buf);
}

int execvp(const char *file, char *const argv[]) {
    int (*real_execvp)(const char *file, char *const argv[]) = dlsym(RTLD_NEXT, "execvp");
    printf("execvp: %s\n", file);
    for (int i = 0; argv[i] != NULL; i++) {
        printf("arg %d: %s\n", i, argv[i]);
    }
    return real_execvp(file, argv);
}

int system(const char *command) {
    int (*real_system)(const char *command) = dlsym(RTLD_NEXT, "system");
    printf("system: %s\n", command);
    return real_system(command);
}


FILE* fopen(const char *filename, const char *mode) {
    FILE* (*real_fopen)(const char *filename, const char *mode) = dlsym(RTLD_NEXT, "fopen");
    printf("fopen: %s %s\n", filename, mode);
    return real_fopen(filename, mode);
}


// gcc -shared -fPIC -o ld_preload.so ld_preload.c