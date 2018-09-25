#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
	srand((int)time(NULL)/10);
	for(int i=0; i<100; i++)
		printf("%d\n", rand());
	return 0;
}
