#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*大域変数（複数の関数から参照される）*/
char *tp; //トークンへのポインタ
char delim[] = " \t\r\n"; //トークンの区切り文字（ここではスペース，タブ，改行）

/*関数プロトタイプ宣言*/
void nextToken(void);
int match(char *);

int main(int argc, char ** argv) {
	FILE *fp; //ファイルポインタ
	char fileName[ ] = "./input.txt"; //開くファイル名
	char *s; //ファイル内容を格納するための文字配列へのポインタ
	fpos_t size; //ファイルサイズを格納する変数
	char c;
	int i;

	/*ファイルを開く*/
	fp = fopen(fileName, "rb");
	if(fp == NULL) { //開けなかったときのエラー処理
		printf("file open error! : %s\n", fileName);
		return -1;
	}

	/*ファイルの終端位置にポインタを移動する*/
	fseek(fp, 0, SEEK_END);

	/*ファイルサイズを変数sizeに取得する*/
	fgetpos(fp, &size);

	/*ファイルサイズ＋1バイトの文字配列を確保*/
	/*（＋1は最後のヌル文字の分．これがないとstrtokが文字列の最後を検出できない）*/
	//s = (char *)malloc((size_t)(size.__pos + 1)*sizeof(char));//PCルーム環境でのgccの場合
	//Windowsや64bit linuxの場合は下のようにする
	s = (char *)malloc((size_t)(size + 1)*sizeof(char));

	if (s == NULL) { //確保失敗のときのエラー処理
		printf("malloc failed!\n");
		return(-1);
	}

	/*ファイルポインタをファイル先頭に移動しファイル内容を読み込む*/
	fseek(fp, 0, SEEK_SET);
	for (i = 0; (c = (char)getc(fp)) != EOF; i++) {
		s[i] = c;
	}
	s[i] = '\0'; //最後にヌル文字を入れる
	fclose(fp); //ファイルを閉じる

	/*最初のトークンを認識*/
	tp = strtok(s, delim);
	
	/*トークンを順に表示*/
	while (tp != NULL) {
		printf("%s\n", tp);
		nextToken();
	}

	free(s);//mallocで確保したメモリを解放
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
