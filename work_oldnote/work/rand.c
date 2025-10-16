#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main(void){
  int a[100];
  int i=0;
  FILE *fp;

  srand((unsigned int)time(NULL));
  for(int j=0;j<100;j++){
    a[j]=rand()%200+1;
  }

  fp=fopen("sample.txt","w");

  while(1){
    fprintf(fp,"%d",a[i]);
    i=i+1;
    if(i>=100){
      break;
    }
    fprintf(fp, "\n");
  }
  fclose(fp);
}
