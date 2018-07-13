//============================================================================
// Name        : FuzzingWrapper.cpp
// Author      : Dorian Knoblauch
// Version     :
// Copyright   : Fraunhofer Fokus
// Description : Test File
//============================================================================

#include "FuzzingWrapper.hpp"

using namespace std;

int main() {
	hexreader_test();
	syscall_test();
}

int hexreader_test(){
	f_readFile("../fuzzing-integration/fuzzdata/coap.txt");
	while(f_hasLine()){
		char *line = f_readLine();
		printf("%s", line);
	}
	f_closeFile();
	return 0;
}

int syscall_test(){
	char *pwd_out = f_syscall("pwd");
	printf("%s", pwd_out);
	return 0;
}
