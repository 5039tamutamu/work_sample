//1w192241-2  田村英之　課題1

#include <stdio.h>

int AAA(int n){
  int i;

  if(!(n & 1)) return 0;
  for(i=3; i*i<=n; i+=2){
    if(!(n % i)) return 0;
  }
  return 1;
}

int BBB(int n){
  int a = n + !(n & 1), b = n - !(n & 1);

  if(n <= 2) return 2;
  while(!AAA(b)){
    if(AAA(a)) return a;
    a += 2;
    b -= 2;
  }
  return b;
}

int main(void){
  int n;
  printf("Input the number: "); //整数を入力する
  scanf("%d", &n); //入力を読み込む

  printf("%d\n", BBB(n)); //表示させる

  return 0;
}
