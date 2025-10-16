//1w192241-2  田村英之　必修課題2


#include <stdio.h>

#define N  1000  //Nを定数として宣言

int main(void){
  int i;
  double x[N], f[N], g[N-1];

  //  存在するファイイルを開き、読み込む
  FILE* fp_in = fopen("Input.txt", "r");  //"r"で読み込みモード
  for(i=0; i<N; i++){
    fscanf(fp_in, "%lf%lf", &x[i], &f[i]);
  }
  fclose(fp_in);

  FILE* fp_out = fopen("Output.txt", "w");
  for(i=0; i<N-1; i++){
    g[i]=(f[i+1]-f[i])/(x[i+1]-x[i]);
    fprintf(fp_out, "%f\t%f\n", x[i], g[i]);
  }
  fclose(fp_out);

  return 0;
}
