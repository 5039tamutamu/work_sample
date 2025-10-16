#include <stdio.h>
int main(void){
  int a, b, c, Sum;
  printf("Input three integers: \n");
  printf("a: ");
  scanf("%d", &a);
  printf("b: ");
  scanf("%d", &b);
  printf("c: ");
  scanf("%d", &c);

  Sum = a + b + c;
  printf("Sum is %d\n", Sum);

  return 0;
}
