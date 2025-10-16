#include <stdio.h>
#define row 2
#define col 2

int main(void){

  int i, j, a, b, c, d, detA;

  printf("Input integer a: ");
  scanf("%d", &a);
  printf("Input integer b: ");
  scanf("%d", &b);
  printf("Input integer c: ");
  scanf("%d", &c);
  printf("Input integer d: ");
  scanf("%d", &d);

  int A[row][col] = {{a, b}, {c, d}} ;

  printf("A=\n");
  for(i=0; i<row; i++){
    for(j=0; j<col; j++){
      printf("%3d", A[i][j]);
      }
    printf("\n");
  }

  detA = ( a * d ) - ( b * c );
  printf("detA is %d.\n", detA);

  return 0;
}
