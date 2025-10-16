#include <stdio.h>
int main(void){
  int a, b, c;

  printf("Input an integer: ");
  scanf("%d", &a);
  b=2*a;
  printf("Twice %d is %d\n", a, b);
  c=3*a;
  printf("Three times %d is %d", a, c);
  return 0;
}
