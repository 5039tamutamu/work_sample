#include <stdio.h>
int main(void){
  int a, b, c, d;
  double e;
  printf("Input three integers: \n");
  printf("a: ");
  scanf("%d", &a);
  printf("b: ");
  scanf("%d", &b);
  printf("c: ");
  scanf("%d", &c);

  d = a + b + c;
  e =(double) d/3;

  printf("Sum is %d, Average is %.1f .", d, e);
  return 0;
}
