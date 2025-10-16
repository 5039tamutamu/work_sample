#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* 円周率（math.hで定義されていないことがあるため */
#define PI 3.1415926535897932384

/*大域変数（複数の関数から参照される）*/
char *tp; //トークンへのポインタ
char delim[] = " \t\r\n"; //トークンの区切り記号

/*現在位置，向き，歩幅，向きの増分を保持する構造体*/
struct Point {
	double x;//x座標
	double y;//y座標
	double a;//向き（x軸からの角度）
	double stp;//歩幅
	double da;//aの増分
};

/*関数プロトタイプ宣言*/
void nextToken(void);
int match(char *);
void push(struct Point);
struct Point pop(void);

int main(int argc, char ** argv) {
	/* ファイル入出力関係の変数 */
	FILE *infp; //入力ファイルへのポインタ
	char InFileName[] = "./input.txt"; //入力ファイル名を格納する文字配列
	char *s; //入力ファイルの内容を格納する文字配列へのポインタ
	fpos_t size; //入力ファイルのサイズ（バイト数）を格納する変数
	FILE *outfp; //出力ファイルへのポインタ
	char OutFileName[256]; //出力ファイル名を格納する文字配列
	char c;
	int i, j;

	/* 図形を描く際のパラメータ */
	struct Point pt; //パラメータを保持する構造体
	double nx, ny; //1歩進んだときの位置を保存する一時変数
	double stp_growth = 0.01;
	double da_growth = 0.06;


	/*入力ファイルを開く*/
	infp = fopen(InFileName, "rb");
	if(infp == NULL) { //開けなかったときのエラー処理
		printf("input file open error! : %s\n", InFileName);
		return -1;
	}

	/*入力ファイルの終りにポインタを移動する*/
	fseek(infp, 0, SEEK_END);

	/*入力ファイルのサイズ（バイト数）を変数sizeに取得する*/
	fgetpos(infp, &size);

	/*入力ファイルサイズ＋1バイト分の文字配列を確保*/
	/*（＋1は最後のヌル文字の分．これがないとstrtokが文字列の最後を検出できない）*/
	s = (char *)malloc((size_t)(size.__pos + 1)*sizeof(char));
	//Windowsや64bit linuxの場合は下のようにする
	//s = (char *)malloc((size_t)(size + 1)*sizeof(char));
	if (s == NULL) { //確保失敗のときのエラー処理
		printf("malloc failed!\n");
		return(-1);
	}

	/* 100コマ分のアニメーションデータを作り，出力ファイルoutput0.dat～output99.datに書き込む */
	//for (i = 0; i < 100; i++) {

		/*ファイルポインタを入力ファイル先頭に移動しファイル内容を読み込む*/
		fseek(infp, 0, SEEK_SET);
		for (j = 0; (c = (char)getc(infp)) != EOF; j++) {
			s[j] = c;
		}
		s[j] = '\0'; //最後にヌル文字を入れる

		/* 出力ファイルを開く */
		//sprintf(OutFileName, "%s%d%s","output", i, ".dat");//出力ファイル名を文字配列OutFileName内に生成
		//outfp = fopen(OutFileName, "w");

		/*入力ファイルの最初のトークンを認識*/
		tp = strtok(s, delim);

		/* パラメータを保持する構造体の初期化 */
		pt.x = 0; pt.y = 0; pt.a = 0; pt.stp = 2.23;
		pt.da = -3197.0 - (3097.0 - 3197.0)/99.0*(double)i;
		printf("%f\n",pt.da);
		//struct Point pt = {0, 0, 0, 2.23, stp};

		/*トークンを順に読み出して処理*/
		while (tp != NULL) {
			printf("%s\n", tp);//トークンを表示（課題ではここに各トークンに関する処理が入る
			nextToken();//次のトークンに進む
		}
		//fclose(outfp);//出力ファイルを閉じる

	//}
	fclose(infp);//入力ファイルを閉じる
	free(s);
	return 0;

}

/*次のトークンに進む（すなわちtpが次のトークンを指すようにする）関数*/
void nextToken(void) {
	if (tp != NULL) {
		tp = strtok(NULL, delim);
	}
}

/*現在のトークン（tpの指すトークン）が，引数文字列と同じかどうかを判定する関数*/
int match(char *s) {
	if (s == NULL || tp == NULL) {//引数またはtpがNULLだったら0（偽）を返す
		return 0;
	}
	if (strcmp(tp, s) == 0) {
		return 1; //引数文字列と同じなら1（真）を返す
	} else {
		return 0; //そうでなければ0（偽）を返す
	}
}

/* スタック */
#define MAXVAL 10000

struct Point val[MAXVAL]; //スタック用配列
int sp = 0; //スタックポインタ

void push(struct Point p) { //構造体Pointをスタックに退避
	if(sp < MAXVAL){
		val[sp++] = p;
	}else{
		printf("error: stack full\n");//スタックがいっぱいのときのエラーメッセージ
		exit(EXIT_FAILURE);//プログラムを途中終了するライブラリ関数
	}
	return;
}

struct Point pop(void) { //構造体Pointをスタックから復活
	if(0 < sp){
		return val[--sp];
	}else{
		printf("error: stack empty\n");//スタックが空の時のエラーメッセージ
		exit(EXIT_FAILURE);//プログラムを途中終了するライブラリ関数
	}
}
