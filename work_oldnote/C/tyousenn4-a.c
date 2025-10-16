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

// RGB構造体の配列pにGaussぼかしを１回処理をする。
void GaussOne(RGB p[]){
  int  r, g, b, x, y, k;
  RGB A, B, C, D, E, F, G, H, I;
  RGB* q = (RGB*)malloc(sizeof(RGB)*width*height);

  //配列qを動的確保
  for(k=0; k<width*height; k++){
    q[k] = p[k];
  }

  for(x=0; x<width; x++){
    for(y=0; y<height; y++){

      //今回扱う画素のRGB構造体
      A = GetPixel(q, x, y);
      B = GetPixel(q, x+1, y);
      C = GetPixel(q, x-1, y);
      D = GetPixel(q, x, y+1);
      E = GetPixel(q, x, y-1);
      F = GetPixel(q, x+1, y+1);
      G = GetPixel(q, x-1,y+1);
      H = GetPixel(q, x+1, y-1);
      I = GetPixel(q, x-1, y-1);

      //今回のアルゴリズム
      r = (2 * (B.r + C.r + D.r + E.r) + F.r + G.r + H.r + I.r + 4 * A.r) / 16;
      g = (2 * (B.g + C.g + D.g + E.g) + F.g + G.g + H.g + I.g + 4 * A.g) / 16;
      b = (2 * (B.b + C.b + D.b + E.b) + F.b + G.b + H.b + I.b + 4 * A.b) / 16;

      //r, g, bの値の補正
      p[y*width + x].r = Bound(r, 0, 255);
      p[y*width + x].g = Bound(g, 0, 255);
      p[y*width + x].b = Bound(b, 0, 255);
    }
  }

  //配列qを解放
  free(q);
}

int main(){

  //ファイルを開き、RGB構造体の配列を取得
  RGB* picture1 = LoadPPM("kinshibai.ppm");
  //printf("%d %d", width, height);

  //RGB構造体の配列picture1にGaussぼかしを１回処理をする
  GaussOne(picture1);

  // RGB構造体の配列picture1をファイルに出力
  SavePPM("gaussOne.ppm", picture1);

  // RGB構造体の配列picture1を解放
  free(picture1);


  //ファイルを開き、RGB構造体の配列を取得
  RGB* picture2 = LoadPPM("kinshibai.ppm");

  //RGB構造体の配列picture2にGaussぼかしを１0回処理をする
  for(int i=0; i<10; i++){
    GaussOne(picture2);
  }

  // RGB構造体の配列picture2をファイルに出力
  SavePPM("gaussTen.ppm", picture2);

  // RGB構造体の配列picture2を解放
  free(picture2);

  return 0;
}
