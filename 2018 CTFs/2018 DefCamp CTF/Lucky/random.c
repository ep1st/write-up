#include <stdio.h>
#include <stdlib.h>

int main() {
	srand(0x61616161);
	for(int i=0; i<100; i++)
		printf("%d\n", rand());
	return 0;
}
