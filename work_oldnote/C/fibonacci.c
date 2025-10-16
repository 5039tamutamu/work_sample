//1w192241-2  田村英之　挑戦課題a


#include <stdio.h>

//再帰除去
int Fibonacci_forloop(int n){
  int i, fn, fn1=1, fn2=0;
  //場合分け
  if(n==0){
    return 0; // n=0のときは0をかえす
  }else if(n==1){
    return 1; // n=1のときは1をかえす
  }else{
    for(i=2; i<=n; i++){
      fn = fn1 + fn2;
      fn2 = fn1;
      fn1 = fn;
    }
    return fn;
  }
}

//再帰
int Fibonacci_recursive(int n){
  //場合分け (再帰除去と同様に)
  if(n==0){
    return 0;
  }else if(n==1){
    return 1;
  }else{
    return Fibonacci_recursive(n-1)+Fibonacci_recursive(n-2);
  }
}

int main() {
  // printfで18番目を表示させる
  printf("f_17 (for loop) = %d\n", Fibonacci_forloop(17));
  printf("f_17 (recursive) = %d\n", Fibonacci_recursive(17));
  return 0;
}
