//1w192241-2  田村英之　必修課題1

#include <stdio.h>
#include <stdlib.h>

int width, height;

typedef struct{
  int r, g, b; //構造体の中身
} RGB; //構造体の名前

//min < n < maxの関数
int Bound(int n, int min, int max){
  if (n<min){
    return min;
  }else if (n>max){
    return max;
  }else{
    return n;
  }
}

//配列の座標の構造体の関数
RGB GetPixel(RGB picture[], int x, int y){
  x = Bound(x, 0, width-1);
  y = Bound(y, 0, height-1);
  return picture[y*width + x];
}

// filenameで指定したファイルを読み込む
RGB* LoadPPM(char filename[]){
  int k, max;
  char format[3];
  FILE* fp = fopen(filename, "r");

  // 画像の横幅と縦幅を読み取る
  fscanf(fp, "%s", format);
  fscanf(fp, "%d%d", &width, &height);
  fscanf(fp, "%d", &max);

  // サイズwidth*heightのRGB構造体の配列を動的確保
  RGB* ppmdata = (RGB*)malloc(width*height*sizeof(RGB));

  // 読み取ったデータの格納
  for(k=0; k<width*height; k++){
    fscanf(fp, "%d%d%d", &ppmdata[k].r, &ppmdata[k].g, &ppmdata[k].b);
  }
  fclose(fp);
  return ppmdata;
}

// RGB構造体の配列ppmdataをファイル名filenameに書き込む
void SavePPM(char filename[], RGB ppmdata[]){
  int k;
  FILE* fp = fopen(filename, "w");
  fprintf(fp, "P3\n%d %d\n255\n", width, height);
  for(k=0; k<width*height; k++){
    RGB rgb = ppmdata[k];
    fprintf(fp, "%d %d %d\n", rgb.r, rgb.g, rgb.b);
  }
  fclose(fp);
}

// RGB構造体の配列pにグレースケール処理をする。
void Grayscale(RGB p[]){
  int  r, g, b, x, y, k, avg;
  RGB c;
  RGB* q = (RGB*)malloc(sizeof(RGB)*width*height);

  //配列qを動的確保
  for(k=0; k<width*height; k++){
    q[k] = p[k];
  }

  for(x=0; x<width; x++){
    for(y=0; y<height; y++){

      //今回扱う画素のRGB構造体
      c = GetPixel(q, x, y);

      //今回のアルゴリズム
      avg= (306*c.r + 601*c.g + 117*c.b)/1024;
      r = avg;
      g = avg;
      b = avg;

      //r, g, bの値の補正
      p[y*width + x].r = Bound(r, 0, 255);
      p[y*width + x].g = Bound(g, 0, 255);
      p[y*width + x].b = Bound(b, 0, 255);
    }
  }

  //配列qを解放
  free(q);
}


// RGB構造体の配列pに減色処理をする。
void Posterization(RGB p[]){
  int  r, g, b, x, y, k;
  RGB c;
  RGB* q = (RGB*)malloc(sizeof(RGB)*width*height);

  //配列qを動的確保
  for(k=0; k<width*height; k++){
    q[k]=p[k];
  }

  for(x=0; x<width; x++){
    for(y=0; y<height; y++){

      //今回扱う画素のRGB構造体
      c = GetPixel(q, x, y);

      //今回のアルゴリズム
      if(c.r <= 127){
        r=0;
      }else{
        r=255;
      }
      if(c.g <= 127){
        g=0;
      }else{
        g=255;
      }
      if(c.b <= 127){
        b=0;
      }else{
        b=255;
      }

      //r, g, bの値の補正
      p[y*width + x].r = Bound(r, 0, 255);
      p[y*width + x].g = Bound(g, 0, 255);
      p[y*width + x].b = Bound(b, 0, 255);
    }
  }

  //配列qを解放
  free(q);
}

int main(void){

  //ファイルを開き、RGB構造体の配列を取得
  RGB* picture1 = LoadPPM("mandrill.ppm");
  //printf("%d %d", width, height);

  //RGB構造体の配列picture1にグレースケール処理をする
  Grayscale(picture1);

  // RGB構造体の配列picture1をファイルに出力
  SavePPM("grayscale.ppm", picture1);

  // RGB構造体の配列picture1を解放
  free(picture1);


  //ファイルを開き、RGB構造体の配列を取得
  RGB* picture2 = LoadPPM("mandrill.ppm");

  //RGB構造体の配列picture2に減色処理をする
  Posterization(picture2);

  // RGB構造体の配列picture2をファイルに出力
  SavePPM("posterization.ppm", picture2);

  // RGB構造体の配列picture2を解放
  free(picture2);

  return 0;
}
