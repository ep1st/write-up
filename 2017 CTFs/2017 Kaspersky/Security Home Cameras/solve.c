#include <stdio.h>
#include <stdlib.h>

int main(void) {
	unsigned char byte;	

	FILE* f_in 	= fopen("secret_encrypted.png","rb");
	FILE* f_out	= fopen("output.png","wb");

	while((byte = fgetc(f_in))!=EOF) {
		byte = ~byte;
		fputc(byte, f_out);
	}
	fclose(f_in);
	fclose(f_out);
	return 0;
}
