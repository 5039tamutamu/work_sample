#include <stdio.h>
#include <string.h>

#define	NODES	16			// 状態の総数 2^4 = 16
#define	LEFT	0			// 左岸にいる状態
#define	RIGHT	1			// 右岸にいる状態

struct NODE {				// 状態を表す構造体（配列は経路を表す）
	int T, W, G, C;			// T, W, G, C はそれぞれ LEFT, RIGHT のいずれか
} node[NODES];

int answers = 0;			// 解の個数

int
inhibit(nd)				// 禁止状態のチェック：
	struct NODE *nd;		// 　W, C のいずれかと G が T と同じ側にいない
{
	return ((nd->T != nd->G) && ((nd->T != nd->W) || (nd->T != nd->C)));
}

int
previous(nd)				// 探索済みのチェック
	struct NODE *nd;
{
	struct NODE *prev;
	for (prev = node; prev != nd; prev++)
		if (	(prev->T == nd->T) &&
			(prev->W == nd->W) &&
			(prev->G == nd->G) &&
			(prev->C == nd->C) ) return(1);
	return(0);
}

int
final_state(nd)				// 目標状態かのチェック
	struct NODE *nd;
{
	return ((nd->T == RIGHT) &&
		(nd->W == RIGHT) &&
		(nd->G == RIGHT) &&
		(nd->C == RIGHT));
}

void
print_member(nd, lr)			// 片岸にいるメンバーの出力
	struct NODE *nd; int lr;	// lr は LEFT, RIGHT のいずれか
{
	printf("[");
	if (nd->T == lr) printf("T"); else printf(" ");
	if (nd->W == lr) printf("W"); else printf(" ");
	if (nd->G == lr) printf("G"); else printf(" ");
	if (nd->C == lr) printf("C"); else printf(" ");
	printf("]");
}

void
print_answer(final)			// 見つかった解答の出力
	struct NODE *final;
{
	struct NODE *nd;
	int Time;
	Time = 0;
	printf("*** Answer #%d ***\n", ++answers);

	for (nd = node; nd <= final; nd++) {
		printf("%5d.  ", nd-node);
		print_member(nd, LEFT);
		if(nd>0){
			if(nd->T != (nd-1)->T)	Time += 2;
			else if(nd->W != (nd-1)->W) Time += 3;
			else if(nd->G != (nd-1)->G) Time += 4;
			else if(nd->C != (nd-1)->C) Time += 5;
			else Time += 5;
		}
		if (nd == final)	printf("  ====  ");
		else if (nd->T == LEFT)	printf("  ===>  ");
		else			printf("  <===  ");

		print_member(nd, RIGHT);
		printf("\n");
	}
	printf("\n The time is %d .\n", Time);
	printf("\n");
}

void
search(nd)				// 探索の再帰手続き（深さ優先探索）
	struct NODE *nd;
{
	struct NODE *next = nd + 1;
	int T = nd->T;

	if (final_state(nd)) {		// 目標状態なら結果を出力して探索を続ける。
		print_answer(nd);
		return;
	}
	if (inhibit(nd) || previous(nd)) return;
			// 禁止状態、すでに訪れた状態なら戻る（別経路の探索を続ける）

	next->T = 1 - T;			// T は必ず移動する
	next->W = nd->W;
	next->G = nd->G;
	next->C = nd->C;
	search(next);				// T 以外は移動しない場合

	if (nd->W == T) {			// T と W が移動する場合
		next->W = 1-T;
		search(next);
		next->W = T;
	}
	if (nd->G == T) {			// T と G が移動する場合
		next->G = 1-T;
		search(next);
		next->G = T;
	}
	if (nd->C == T) {			// T と C が移動する場合
		next->C = 1-T;
		search(next);
		next->C = T;
	}
}

void
main(argc, argv)
	int argc; char **argv;
{
	/* 初期状態では T, W, G, C すべてが左岸にいる */
	node->T = node->W = node->G = node->C = LEFT;

	search(node);				// 探索手続きの起動
}