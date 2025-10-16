#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(void){
  char Seiza[100];
  printf("Input your Seiza: ");
  scanf("%s", Seiza);

  char fortune[3][100]={"Very Lucky", "Lucky", "Not Good"};

  int a;
  srand((unsigned) time(NULL));
  a = (int) (rand()/(RAND_MAX+1.0)*3);
  printf("Today is %s.\n", fortune[a], a+1);

  return 0;
}
