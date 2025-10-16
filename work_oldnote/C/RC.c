//1w192241-2  田村英之　必修課題1


#include <stdio.h>
#include <math.h>

//グローバル関数を用いる
double dV_dt(double V){
  //定数の指定
  double Vin = 3;
  double C = 0.000050;
  double R = 2241000;
  double dV_dt;
  dV_dt = ( Vin - V ) / ( R * C );
  //戻り値の言及
  return dV_dt;
}

int main(void){
  //ファイルを作成
  FILE* fp = fopen("Output1.txt", "w");
//定数の指定
  double dt[4] = {0.1, 10, 100, 200};
  double V1, V2, V3, V4;

  V1 = 0.0;
  V2 = 0.0;
  V3 = 0.0;
  V4 = 0.0;

  for(int x = 0; x < 20000; x++){
    fprintf(fp, "%f\t%f", (double)x/10.0, V1);
    V1 += dt[0] * dV_dt(V1);
    if(x%10 == 0){
      fprintf(fp, "\t%f", V2);
      V2 += dt[1] * dV_dt(V2);
    }
    if(x%100 == 0){
      fprintf(fp, "\t%f", V3);
      V3 += dt[2] * dV_dt(V3);
    }
    if(x%200 == 0){
      fprintf(fp, "\t%f", V4);
      V4 += dt[3] * dV_dt(V4);
    }
    //表示させる
    fprintf(fp, "\n");

  }
  //ファイルを閉じる
  fclose(fp);

  return 0;
}
