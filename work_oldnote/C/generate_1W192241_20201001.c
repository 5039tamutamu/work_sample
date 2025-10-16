//1w192241-2  田村英之　課題

#include <stdio.h>
#include <string.h>

/* バッファ配列のサイズ */
#define BUFSIZE 500000

/* 置き換えの繰り返し回数 */
/* あまり大きな値にすると，バッファ配列をはみ出す恐れあり */
#define N_REPLACE 40
int main() {
	FILE *fp; /*ファイルポインタ*/
	char filename[] = "input.txt"; /*出力ファイル名*/
	int i;

	/* バッファ配列およびアクセス用ポインタ */
	/* バッファ配列をはみ出すとプログラムは正常動作しないので注意 */
	char buf[BUFSIZE];
	char tmp[BUFSIZE];
	char *bp, *tp;

	/* 書き換え記号列 */
	char start[] = "C C C";//初期文字列
	char C_to[] = "! < [ ) B | V F C ]";//書き換え文字列
  char B_to[] = "A | B F !";//書き換え文字列
  char A_to[] = "F | - A | + F";//書き換え文字列
  char V_to[] = "+";//書き換え文字列

	strcpy(buf, start);
	for(i = 0; i < N_REPLACE; i++) {//N_REPLACE回の書き換えを行うループ
		bp = buf;
		tp = tmp;
		tmp[0] = '\0';
		while (*bp != '\0') {
			switch(*bp) {
				case 'C':
					strcat(tmp, C_to);//書き換える文字列を，配列tmp内の文字列の最後に連結
					tp += strlen(C_to);//連結した文字列分ポインタを進める
					bp++;//配列buf用ポインタも1つ進める
					break;
        case 'B':
  				strcat(tmp, B_to);//書き換える文字列を，配列tmp内の文字列の最後に連結
  				tp += strlen(B_to);//連結した文字列分ポインタを進める
  				bp++;//配列buf用ポインタも1つ進める
					break;
        case 'A':
  				strcat(tmp, A_to);//書き換える文字列を，配列tmp内の文字列の最後に連結
  				tp += strlen(A_to);//連結した文字列分ポインタを進める
					bp++;//配列buf用ポインタも1つ進める
  				break;
        case 'V':
  				strcat(tmp, V_to);//書き換える文字列を，配列tmp内の文字列の最後に連結
  				tp += strlen(V_to);//連結した文字列分ポインタを進める
					bp++;//配列buf用ポインタも1つ進める
          break;
				default:
					*tp++ = *bp++;//書き換え対象でない場合はそのままtmpにコピー
					*tp = '\0';//strcatに備える
					break;
			}
		}
		strcpy(buf, tmp);
	}
	printf("length = %lu\n",strlen(buf));//置き換え終了後の文字列の長さを表示

	fp = fopen(filename, "w"); //ファイルを書き込みモードで開く
	fprintf(fp, "%s", buf); //配列bufの内容をファイルに書き込み
	fclose(fp); //ファイルを閉じる

	return 0;
}
