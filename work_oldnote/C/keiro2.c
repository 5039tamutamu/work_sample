//1w192241-2  田村英之　必修課題2

#include <stdio.h>

//グローバル関数を用いる。
int CountRout(int x, int y, int n){
  //各定数の範囲の指定
  0 <= x <4;
  0 <= y < 4;
  n < 11;

  //場合分けする
  if( n == 0 ){
    return 0;
  }else if( x == -1 || y == -1 || x == 4 || y == 4 ){
    return 0;
  }else if( ( x == 3 - n && y == 3 ) || ( x == 3 && y == 3 - n ) ){
    return 1;
  }else{
    return CountRout(x+1, y, n-1) + CountRout(x, y+1, n-1) + CountRout(x-1, y, n-1) + CountRout(x, y-1, n-1);
  }
}

int main(void){
  int A = CountRout(0, 0, 10);
  printf("%d\n", A);
  return 0;
}
