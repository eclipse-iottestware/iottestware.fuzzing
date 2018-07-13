#include "hexreader.hh"

FILE * fp;
char * line = NULL;
size_t len = 0;
ssize_t read = 0;

int f_readFile(const char* path) {
	fp = fopen(path, "r");
	if (fp == NULL) {
		printf("Exit on path:%s", path);
		return false;
	}
	return true;
}

int f_hasLine() {
	return ((read = getline(&line, &len, fp)) != -1);
}
char *f_readLine() {
	size_t size = strlen(line) + sizeof(char);
	char* rtn = (char*) malloc(size);
	strncpy( rtn, line, size);
	rtn[size-1]='\0';
	line[size-2]='\0';
	return line;
}

int f_closeFile() {
	fclose(fp);
	if (line) {
		free(line);
	}
	return 0;
}
