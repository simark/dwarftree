#include <stdio.h>
#include <string.h>

int (*ptr_to_func_taking_char_and_float_and_returning_int)(char, float);
int (**ptr_to_ptr_to_func_taking_char_and_float_and_returning_int)(char, float);

volatile int c;

int func1(char a, float b) {
	printf("ALLO %c %f!\n", a, b);

	return 0;
}

struct bobby {
	char tables;
	int roflmao;
};

const float xxx() {
    return 1.2f;
}

int main() {
	struct bobby a;
	a.roflmao = 3;
	xxx();

	ptr_to_func_taking_char_and_float_and_returning_int = func1;


	ptr_to_ptr_to_func_taking_char_and_float_and_returning_int = &ptr_to_func_taking_char_and_float_and_returning_int;

	ptr_to_func_taking_char_and_float_and_returning_int('a', 1.0f);
	(*ptr_to_ptr_to_func_taking_char_and_float_and_returning_int)('b', 2.0f);

	return a.roflmao;
}
