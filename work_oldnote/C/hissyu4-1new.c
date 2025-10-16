//1w192241-2  田村英之　必修課題1

#include <stdio.h>
#include <stdlib.h>

int width, height;

typedef struct{
  int r, g, b; //構造体の中身
} RGB; //構造体の名前

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

RGB* Grayscale(RGB* ppmpixel){
  RGB* gray_ppmpixel;
  gray_ppmpixel = (RGB*)malloc(sizeof(RGB)*width*height);
  for(int i=0; i<width*height; i++){
    int avg= (306* ppmpixel[i].r + 601* ppmpixel[i].g + 117* ppmpixel[i].b)/1024;
    gray_ppmpixel[i].r = avg;
    gray_ppmpixel[i].g = avg;
    gray_ppmpixel[i].b = avg;
  }
  return gray_ppmpixel;
}

RGB* Posterization(RGB* ppmpixel){
  RGB* posterization_ppmpixel;
  posterization_ppmpixel = (RGB*)malloc(sizeof(RGB)*width*height);
  for(int i=0; i<width*height; i++){
    if(ppmpixel[i].r <= 127){
      posterization_ppmpixel[i].r = 0;
    }else{
      posterization_ppmpixel[i].r = 255;
    }
    if(ppmpixel[i].g <= 127){
      posterization_ppmpixel[i].g = 0;
    }else{
      posterization_ppmpixel[i].g = 255;
    }
    if(ppmpixel[i].b <= 127){
      posterization_ppmpixel[i].b = 0;
    }else{
      posterization_ppmpixel[i].b = 255;
    }
  }
  return posterization_ppmpixel;
}

int main(void){
  RGB* picture = LoadPPM("mandrill.ppm");
  RGB* picture1 = Grayscale(picture);
  RGB* picture2 = Posterization(picture);

  SavePPM("grayscale1.ppm", picture1);
  SavePPM("posterization1.ppm", picture2);

  free(picture);
  free(picture1);
  free(picture2);

  return 0;
}
