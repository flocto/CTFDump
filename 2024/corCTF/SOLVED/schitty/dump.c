/** Copyright 2019 - Intika <intika@librefox.org>
 * Replace ******** with secret read from fd 21
 * Also change arguments location of sub commands (sh script commands)
 * gcc -Wall -fpic -shared -o shc_secret.so shc_secret.c -ldl
 * */
#define _GNU_SOURCE /* needed to get RTLD_NEXT defined in dlfcn.h */
#define PLACEHOLDER "********"
#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
static char secret[128000]; //max size
typedef int (*pfi)(int, char **, char **);
static pfi real_main;
// copy argv to new location
char **copyargs(int argc, char** argv){
    char **newargv = malloc((argc+1)*sizeof(*argv));
    char *from,*to;
    int i,len;
    for(i = 0; i<argc; i++){
        from = argv[i];
        len = strlen(from)+1;
        to = malloc(len);
        memcpy(to,from,len);
        // zap old argv space
        memset(from,'\0',len);
        newargv[i] = to;
        argv[i] = 0;
    }
    newargv[argc] = 0;
    return newargv;
static int mymain(int argc, char** argv, char** env) {
    //fprintf(stderr, "Inject main argc = %d\n", argc);
    return real_main(argc, copyargs(argc,argv), env);
int __libc_start_main(int (*main) (int, char**, char**),
                      int argc,
                      char **argv,
                      void (*init) (void),
                      void (*fini)(void),
                      void (*rtld_fini)(void),
                      void (*stack_end)){
    static int (*real___libc_start_main)() = NULL;
    int n;
    if (!real___libc_start_main) {
        real___libc_start_main = dlsym(RTLD_NEXT, "__libc_start_main");
        if (!real___libc_start_main) abort();
    n = read(21, secret, sizeof(secret));
    if (n > 0) {
      int i;
    if (secret[n - 1] == '\n') secret[--n] = '\0';
    for (i = 1; i < argc; i++)
        if (strcmp(argv[i], PLACEHOLDER) == 0)
          argv[i] = secret;
    real_main = main;
    return real___libc_start_main(mymain, argc, argv, init, fini, rtld_fini, stack_end);