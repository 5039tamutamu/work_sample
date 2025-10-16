//1w192241-2  田村英之　課題2

#include <stdio.h>
#include <string.h>


int main(void){
  int i, j, k, n, N;
  char *terms[20], *temp;

  FILE* fp_in = fopen("lan.txt", "r");
  while(fscanf(fp_in, "%s", terms[n])!=EOF){
    n++;
    printf("%d\n", n);
  }
  fclose(fp_in);

  FILE* fp_out = fopen("Output2.txt", "w");
  N = sizeof(terms)/sizeof(terms[0]);
  N--;

  for(i=0; i<N; i++){
    for(j=i+1; j<N; j++){
      if(strcmp((terms[i]), (terms[j]))>0){
        temp = *(terms+i);
        *(terms+i) = *(terms+j);
        *(terms+j) = temp;
      }
    }
  }

  for(k=0; k<n; k++){
    fprintf(fp_out, "%s\n", terms[k]);
  }

  fclose(fp_out);

  return 0;
}
