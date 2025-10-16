//1w192241-2  田村英之　必修課題2


#include <stdio.h>

int CountRout(int x, int y, int n){
  if(x == 3 && y == 3 && n == 0 ){
    return 1;
  }else if( n == 0 ){
    return 0;
  }else if( x == 0 ){
    if( y == 0 ){
      return CountRout(x+1, y, n-1) + CountRout(x, y+1, n-1);
    }else if( y == 3 ){
      return CountRout(x+1, y, n-1) + CountRout(x, y-1, n-1);
    }else{
      return CountRout(x+1, y, n-1) + CountRout(x, y+1, n-1) + CountRout(x, y-1, n-1) ;
    }
  }else if( x == 3 ){
    if( y == 0 ){
      return CountRout(x-1, y, n-1) + CountRout(x, y+1, n-1);
    }else if( y == 3 ){
      return CountRout(x+1, y, n-1) + CountRout(x, y-1, n-1);
    }else{
      return CountRout(x-1, y, n-1) + CountRout(x, y+1, n-1) + CountRout(x, y-1, n-1) ;
    }
  }else if( y == 0 ){
    if(x != 0 && x != 3 ){
      return CountRout(x+1, y, n-1) + CountRout(x-1, y, n-1) + CountRout(x, y+1, n-1) ;
    }
  }else if( y == 3 ){
    if(x != 0 && x != 3 ){
      return CountRout(x+1, y, n-1) + CountRout(x-1, y, n-1) + CountRout(x, y-1, n-1) ;
    }
  }else{
    return CountRout(x+1, y, n-1) + CountRout(x-1, y, n-1) + CountRout(x, y+1, n-1) + CountRout(x, y-1, n-1) ;
  }
}

int main(void){
  printf("%d", CountRout(0,0,10));
  return 0;
}
