#include <stdio.h>
int main(void){
  int N, SN, angN;
  printf("Input integer: ");
  scanf("%d", &N);

  if (N>=3){
    SN = 180 * ( N - 2 );
    printf("The sum of the inner angles is %d.\n", SN);
    angN = SN / N;
    printf("The size of one angle is %d.\n", angN);
  }else{
    printf("Impossible to calculate\n");
  }

  return 0;
}
