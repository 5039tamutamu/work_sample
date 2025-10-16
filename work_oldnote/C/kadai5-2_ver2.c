//1w192241-2  田村英之　課題2

#include <stdio.h>
#include <string.h>

#define N 30
#define M 20

int AA(char *a, char *A){
  char b, B;
  for(;;){
    b = *a;
    B = *A;

    if(b==B){
      a++;
      A++;
    }

    if(*a=='\0')  return 0;

    if(b != B)  return b-B;
  }
}

int main(void){
  int i, j, k, n=0;
  char terms[N][M];
  char tmp[M];

  FILE *fp = fopen("lan.txt", "r");
  while(fscanf(fp, "%s", &terms[n]) != EOF){
    n++;
    printf("%d\n", n);
  }
  fclose(fp);

  for(i=0; i<n-1; i++){
    for(j=i+1; j<n; j++){
      if(AA(terms[i], terms[j])>0){
        strcpy(tmp, terms[i]);
        strcpy(terms[i], terms[j]);
        strcpy(terms[j], tmp);
      }
    }
  }


  fp = fopen("Output2.txt", "w");
  for(k=0; k<n; k++){
    fprintf(fp, "%s\n", terms[k]);
  }
  fclose(fp);

  return 0;
}
