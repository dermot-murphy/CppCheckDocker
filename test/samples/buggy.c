#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int) * 10);
    p[10] = 0;
    return 0;
}
