#include <stdio.h>
int main(void){
  int a,b;
  printf("Input a natural number1: ");
  scanf("%d", &a);
  printf("Input a natural number2: ");
  scanf("%d", &b);
  if(a<b){
    int c=a;
    a=b;
    b=c;
  }
  int tmp, num1=a, num2=b;
  while(num1%num2!=0){
    tmp=num2;
    num2=num1%num2;
    num1=tmp;
  }
  printf("GCD is %d.\n", num2);
  printf("LCM is %d.\n", a*b/num2);
  return 0;
}
