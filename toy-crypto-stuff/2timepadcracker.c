#include <stdio.h>
#include <string.h>

int main() {
    char m1[] = "Someone's sniffing around. Destroy the files!";
    
    int c1[] = {
    	18, 82, 3, 201, 235, 174, 211, 119, 57, 81, 156, 34, 181, 131, 244, 173, 123,
        127, 129, 120, 84, 114, 109, 220, 254, 123, 99, 49, 28, 95, 62, 91, 69, 58, 252,
        216, 43, 184, 214, 62, 49, 171, 153, 168
    };
    
    int c2[] = {
        15, 85, 11, 140, 212, 178, 223, 61, 47, 81, 130, 37, 178, 140, 225, 176, 112,
        106, 134, 106, 6, 110, 104, 215, 255, 54, 43, 85, 16, 95, 106, 70, 68, 99, 189,
        216, 99, 141, 184, 10, 120, 139, 168, 234
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
