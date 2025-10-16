//1w192241-2  田村英之　課題
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

//非終端記号その他を表す定数の定義*/
enum { S, Exp, Tail, Term, Num, Plus, Minus };

struct tnode {
	int type;//非終端記号の種類（S,Exp,Tail,Num)
	int val;//自然数の値や演算の種類の記憶用変数
	struct tnode *left;//左側のノードを指すポインタ
	struct tnode *right;//右側のノードを指すポインタ
};

char *tp;
char delim[] = " \t\r\n";

struct tnode *talloc(int);
void nextToken(void);
int match(char *);
int isnumber(char *);
void parse(struct tnode *);
int exe(struct tnode *);
void err(char *msg);

int main(int argc, char ** argv) {
	FILE *fp; //ファイルポインタ
	char fileName[256] = "./input_calc.txt"; //開くファイル名(inputファイルが多かったため、名前を変更しました)
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
	//演習環境（32bit linux）のときは下のようにする
	//s = (char *)malloc((size_t)(size.__pos + 1)*sizeof(char));
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

	/*最初のトークンを認識*/
	tp = strtok(s, delim);

	/*開始記号ノード（S）を根とし，解析木を生成*/
	root = talloc(S);
	parse(root);

	/*解析木より数式の値を求めて表示*/
	printf("sum = %d\n", exe(root));

	/*mallocで確保したメモリ領域を開放し，ファイルを閉じて終了*/
	free(s);
	fclose(fp);
	return 0;
}
/*パーサ*/
/*
文法
S -> Exp [EOF]
Exp -> Term Tail?
Tail -> [+-] Term Tail?
Term -> Num | ( Exp )
Num -> [0-9]+
*/
void parse(struct tnode *p) {
	if (p->type == S) {// S -> Exp [EOF]
		p->left = talloc(Exp);//左にExpノードを作る
		parse(p->left);//Exp部分の構文解析の実行（左の子に丸投げ）
		if (tp != NULL) { //入力の最後に余計なトークンがあった
			err("S:extra token at the end of input.");
		}
	} else if (p->type == Exp) {// Exp -> Term Tail?
		p->left = talloc(Term);//左にTermノードを作る
		parse(p->left);//Term部分の構文解析の実行（左の子に丸投げ）
		if (match("+") || match("-")) {//Numの後にTailがあるか調べる
			p->right = talloc(Tail);//右にTailノードを作る
			//ここでnextToken()は行わない．行うと右の子が加算／減算を記録できない
			parse(p->right);//Tail部分の構文解析の実行（右の子に丸投げ）
		}
	} else if (p->type == Tail) {// Tail -> [+-] Term Tail?
		if (match("+")) {
			p->val = Plus;//加算を記録
			nextToken();
		} else if (match("-")) {
			p->val = Minus;//減算を記録
			nextToken();
		}
		p->left = talloc(Term);//左にTermノードを作る
		parse(p->left);//Term部分の構文解析の実行（左の子に丸投げ）
		if (match("+") || match("-")) {//Numの後にTailがあるか調べる
			p->right = talloc(Tail);//右にTailノードを作る
			parse(p->right);//Tail部分の構文解析の実行（右の子に丸投げ）
		}
	} else if (p->type == Term) {// Term -> Num | ( Exp )
		if (isnumber(tp)) {//Numかどうか調べる
			p->left = talloc(Num);
			parse(p->left);//左にNumノードを作って丸投げ
		} else if (match("(")) {// ( Exp )かどうか調べる
			nextToken();//次のトークンに進む
			p->left = talloc(Exp);
			parse(p->left);//左にExpノードを作って丸投げ
			//戻ってきたら ) があるか調べる（なければエラー）
			if (match(")")) {
			nextToken();//次のトークンに進む
			//p->left = talloc(Exp);
			//parse(p->left);//左にExpノードを作って丸投げ
			} else {
			err("Term:')' expected.");//エラー「)がなかった」
			}
		} else {
			err("Term:'Num' or '(' expected.");//エラー「数字または ( がなかった」
		}
	} else if (p->type == Num) {// Num -> -?[0-9]+
		if (isnumber(tp)) {//自然数を表す記号列かどうか調べる
			p->val = atoi(tp);//atoi関数により自然数文字列を整数値に変換しvalに格納
			nextToken();
		} else {//自然数ではなかった
			err("Num: number expected.");
		}
	} else {//S, Exp, Num, Tailのいずれでもない
		printf("parse: unknown type: %d\n", p->type);
		exit(EXIT_FAILURE);
	}
}
int isnumber(char *s) {
	if (s == NULL)//引数が無効（偽を返す）
		return 0;

	if (*s == '-')
		s++;     //マイナス符号があったら1文字先に進む	

	if (!isdigit(*s))//最初の文字が数字であるか調べる（数字でなければ偽を返す）
		return 0;
	s++;//次の文字に進む
	while(isdigit(*s))//後に続く数字のチェック
		s++;
	if (*s != '\0')//数字かヌル文字以外の文字があったら偽を返す
		return 0;
	return 1;//何事もなく文字列の終わりに到達（真を返す）
}
/* エグゼキュータ */
int exe(struct tnode *p) {
	int sum = 0;
	if (p->type == S) {
		if (p->left != NULL) {//左にノードがあった場合
			sum += exe(p->left);//左ノードからの値をsumに加算
		}
		return sum;//sumの値を返す
	} else if (p->type == Exp) {
		if (p->left != NULL) {//左にノードがあった場合
			sum += exe(p->left);//左ノードからの値をsumに加算
		}
		if (p->right != NULL) {//右にノードがあった場合
			sum += exe(p->right);//右ノードからの値をsumに加算
		}
		return sum;//sumの値を返す
	} else if (p->type == Tail) {
		if (p->val == Plus) {//加算の場合
			sum += exe(p->left);//左ノードからの値をsumに加算
		} else if (p->val == Minus) {//減算の場合
			sum -= exe(p->left);//左ノードからの値をsumから減算
		}
		if (p->right != NULL) {//右にノードがあった場合
			sum += exe(p->right);//右ノードからの値をsumに加算
		}
		return sum;//sumの値を返す
	} else if (p->type == Term) {
		if(p->left != NULL){  //左にノードがあった場合
		sum += exe(p->left);//左ノードからの値をsumに加算
		}
		return sum;//sumの値をリターン
	} else if (p->type == Num) {
		return p->val;//自然数の数値を返す
	} else {
		printf("exe: unknown type: %d\n", p->type);
		exit(EXIT_FAILURE);
	}
}
/*2分木のノード1つ分のメモリ領域を確保し，その先頭へのポインタを返す関数*/
struct tnode *talloc(int t) {
	struct tnode *p = (struct tnode *) malloc(sizeof(struct tnode));
	p->type = t;
	p->val = 0;
	p->left = NULL;
	p->right = NULL;
	return p;
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
/*エラーメッセージと現在のトークンを表示し，プログラムを途中終了する関数*/
void err(char *msg) {
	if (tp != NULL)
		printf("%s Token: %s\n", msg, tp);
	else
		printf("%s Token: NULL\n", msg);
	exit(EXIT_FAILURE);//プログラムを途中終了するライブラリ関数
}
