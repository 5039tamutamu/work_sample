//1w192241-2  田村英之　課題1

#include <stdio.h>

//素数を探す
int AA(int n){
  int i;

  if(n<=1) return 0;

  for(i=2; i<n; i++){
    if(n%i==0) return 0;
  }
  return 1;
}

//ある数nに対してnより大きい素数と小さい素数で比較する。
void BB(int n){
  int a = n;
  int b = n;
  int c = n;
  int d = n;
  int e, f;

  if((!AA(a)) && (!AA(b))){
    while(!AA(a)){
      a++;
    }while(!AA(b)){
      b--;
    }

    if(a-n > n-b){
      printf("%d\n", b);
    }
    if(a-n < n-b){
      printf("%d\n", a);
    }
    if(a-n == n-b){
      printf("%d %d\n", b, a);
    }
  }

  e = c + 1;
  f = d - 1;

  if((!!AA(c)) && (!!AA(d))){
    while(!AA(e)){
      e++;
    }while(!AA(f)){
      f--;
    }

    if(e-n > n-f){
      printf("%d\n", f);
    }
    if(e-n < n-f){
      printf("%d\n", e);
    }
    if(e-n == n-f){
      printf("%d %d\n", f, e);
    }

  }

}


int main(void){
  int N;
  printf("Input the number: "); //整数を入力する
  scanf("%d", &N); //入力を読み込む

  BB(N);

  return 0;
}
