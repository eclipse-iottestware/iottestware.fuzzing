#include "syscall.hh"

char *f_append_strings(const char * old, const char * _new){
	size_t len = strlen(old) + strlen(_new) + 1;
	char *out = (char*) malloc(len);
	sprintf(out, "%s%s", old, _new);
	return out;
}

char *f_syscall(const char* cmd) {
	char buffer[128];
	char *result =(char*)malloc(0);
	FILE* pipe = popen(cmd, "r");
	try {
		while (!feof(pipe)) {
			if (fgets(buffer, 128, pipe) != NULL)
				result = f_append_strings(result,buffer);
		}
	} catch (...) {
		pclose(pipe);
		throw;
	}
	pclose(pipe);
	return(result);
}
