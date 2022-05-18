#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <sys/unistd.h>
#include <sys/mman.h>

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    puts("the New England special!");

    //  (addr, length, prot, flags, fd, offset)
    // private copy-on-write + 0-init no file
    char *ptr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    // (fd, buf, count)
    ssize_t count = read(stdin, ptr, 0x1000);

    bool pass = true;
    for(int i = 0; i < count; ++i) {
        if (ptr[i] - '0' > 'N') { // unsigned 32 bit cmp of LSB (byte)
            pass = false;
            break;
        }
    }

    if (pass) {
        puts("yummy!");
        strfry(ptr);
        ((void(*)())ptr)();
    } else {
        puts("yuck!");
    }
}
