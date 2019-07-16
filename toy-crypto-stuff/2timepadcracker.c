#include <stdio.h>
#include <string.h>

int main() {
    char m1[] = "Someone's sniffing around. Destroy the files!";
    int c1[] = {
    	104, 136, 105, 94, 68, 35, 79, 32, 182, 241, 81, 42, 251, 19, 89, 152, 180,
    	2, 152, 9, 47, 55, 110, 184, 43, 75, 132, 193, 192, 130, 139, 81, 229, 145,
    	55, 170, 193, 82, 177, 236, 19, 165, 230, 54
    };
    int c2[] = {
    	111, 143, 97, 27, 123, 63, 67, 106, 160, 241, 79, 45, 252, 28, 76, 133, 191,
    	23, 159, 27, 125, 43, 107, 179, 42, 6, 204, 165, 204, 130, 223, 66, 254, 200,
    	68, 151, 253, 23, 160, 187, 66
    };
    int clength = (int)(sizeof(c1) / sizeof(int));
    int r[clength];
    char m2[clength];

    for (int i = 0; i < clength; i++) {
    	r[i] = c1[i] ^ c2[i];
    }

    for (int i = 0; i < clength; i++) {
    	m2[i] = r[i] ^ m1[i];
    } 

    printf("%s\n", m2);

    return 0;
}