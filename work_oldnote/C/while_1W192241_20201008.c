//1w192241-2  田村英之　課題

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

//終端・非終端記号を表す定数の定義（S1, A1を，それぞれ0,1を値に持つ定数とする）*/
//enum { S1, A1 };
//提出課題については，下記のようにすればよい．
enum { S, E, A, Cond, Rel };

/*2分木を表す構造体*/
struct tnode {
	int type;//終端・非終端記号を表す値
	struct tnode *left;//左側のノードを指すポインタ
	struct tnode *right;//右側のノードを指すポインタ
};

/*大域変数（複数の関数から参照される）*/
char *tp; //現在のトークンへのポインタ
char delim[] = " \t\r\n"; //トークンの区切り記号

/*関数プロトタイプ宣言*/
void nextToken(void);
int match(char *s);
struct tnode *talloc(int t);
void err(char *msg);
void parse(struct tnode *p);

/*メイン関数*/
int main(int argc, char ** argv) {
	FILE *fp; //ファイルポインタ
	char fileName[256] = "./input_while.txt"; //開くファイル名
	char *s; //ファイル内容を格納するための文字配列へのポインタ
	fpos_t size; //ファイルサイズを格納する変数
	char c;
	int i;

	struct tnode *root;

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
	//s = (char *)malloc((size_t)(size.__pos + 1)*sizeof(char));
        //Windowsや64bit linuxの場合は下のようにする
        s = (char *)malloc((ftell(fp) + 1)*sizeof(char));
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

	/*最初のトークンを認識*/
	tp = strtok(s, delim);

	/*開始記号ノード（S1）を根とし，解析木を生成*/
	root = talloc(S);
	parse(root);

	free(s);
	fclose(fp);
	return 0;
}
/*
文法
(1)S → E [EOF]
(2)E → A | cmd
(3)A → while ( Cond ) { E }
(4)Cond → eq Rel eq
(5)Rel → < | >
*/
/*パーサ*/
void parse(struct tnode *p) {
	if (p->type == S) {
		p->left = talloc(E);//左側にEノードを作成
		parse(p->left);//Eノードに丸投げ
		if (tp == NULL) {//E部分の解析から戻った後トークンがなければ
			printf("parsing completed\n");//構文解析成功
		} else {//余計なトークンがあったら
			err("S: extra token at the end of input.");//エラー
		}
	} else if (p->type == E) {
		if (match("while")) {//whileで始まっているのでAがある
			p->left = talloc(A);//左側にAノードを作成
			parse(p->left);//Aノードに丸投げ
		} else if (match("cmd")) {
			nextToken();
		} else {
			err("E: 'A' or 'cmd' expected");//「A」または「cmd」がなかった
		}
	} else if (p->type == A) {
		if (match("while")) {
			nextToken();
			if (match("(")) {
				//Condノードを左に作って丸投げ,戻ってきたら')'があるか調べる（なければエラー）
				p->left = talloc(Cond);
				parse(p->left);
				if (match(")")) {
					nextToken();
					//'{'があるか調べる（なければエラー）
					if (match("{")) {
						nextToken();
						//Eノードを右に作って丸投げ,戻ってきたら'}'があるか調べる（なければエラー）
						p->left = talloc(E);
						if (match("}")) {
							nextToken();
						} else {
							err("A: '}' expected after 'E'.");
						}
					} else {
						err("A: '{' expected after ')'.");
					}
				} else {
					err("A: ')' expected after 'Cond'.");
				}
			} else {
			//whileがなかった（実際はEの部分でチェック済みなのでここが実行されることはない
			err("A: 'while' expected");
		}
	}
	} else if (p->type == Cond) {
		nextToken();
		if (match("eq")) {
			p->left = talloc(Rel);
			parse(p->left);
			if (match("eq")) {
				nextToken();
			} else {
				err("Cond: 'eq' expected after 'Rel'.");
			}
		} else {
			err("Cond: 'eq' expected.");
		}
	} else if (p->type == Rel) {
		nextToken();
		if (match("<")||match(">")) {
			nextToken();
		} else {
			err("Rel: '<' or '>' expected.");
		}
	}
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

/*2分木のノード1つ分のメモリ領域を確保し，その先頭へのポインタを返す関数*/
struct tnode *talloc(int t) {
	struct tnode *p = (struct tnode *) malloc(sizeof(struct tnode));
	p->type = t;
	p->left = NULL;
	p->right = NULL;
	return p;
}

/*エラーメッセージと現在のトークンを表示し，プログラムを途中終了する関数*/
void err(char *msg) {
	if (tp != NULL)
		printf("%s Token: %s\n", msg, tp);
	else
		printf("%s Token: NULL\n", msg);
	exit(EXIT_FAILURE);//プログラムを途中終了するライブラリ関数．
}
