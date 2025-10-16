#include <stdio.h>
#include <stdlib.h>

int read[100];
int push[100];
int count;

//100個のファイルデータを読み込む.
void getNum(){
  FILE *fp;
  char fname[]="sample.txt";
  fp=fopen(fname, "r");

  for(int i=0;i<100;i++){
    fscanf(fp,"%d",&read[i]);
  }

  fclose(fp);
}

//ノードの構造体を宣言.
struct node_r{
  int num;
  struct node_r *left;
  struct node_r *right;
};

//ノードを追加するメモリを確保する.
struct node_r *mallocN(int num){
  struct node_r *add;
  add=(struct node_r*)malloc(sizeof(struct node_r));

  add->left=NULL;
  add->right=NULL;
  add->num=num;

  return add;
}

//ノードを追加する.
//引数は, 根のノードと追加する数字.
struct node_r *addN(struct node_r *root, int num){
  struct node_r *node;

  //根のノードに何もない, つまり最初のとき.
  if(root==NULL){
    root=mallocN(num);
    return root;
  }

  //追加する数字が, 注目しているノードの数字よりも小さければ左.
  //追加する数字が, 注目しているノードの数字よりも大きければ右.
  //追加する数字が, 注目しているノードの数字であれば無視.
  node=root;
  while(1){
    if(num < node->num){
      if(node->left==NULL){
        node->left=mallocN(num);
        break;
      }
      node=node->left;
    }
    else if(num > node->num){
      if(node->right==NULL){
        node->right=mallocN(num);
        break;
      }
      node=node->right;
    }
    else{
      break;
    }
  }
  return root;
}

//ノードの値を順番に配列に代入する.
//最初に左を見て, 見つくしたら右を見る.
void pushN(struct node_r *root){
  if(root==NULL){
    return;
  }

  pushN(root->left);
  push[count]=root->num;
  count=count+1;
  pushN(root->right);
  return;
}

//存在するか探す.
void search(struct node_r *root, int N){
  if(root==NULL){
    printf("二分探索木に%dは存在しません.\n\n",N);
    return;
  }
  else if(N < root->num){
    search(root->left,N);
  }
  else if(N > root->num){
    search(root->right,N);
  }
  else if(N==root->num){
    printf("二分探索木に%dは存在します.\n\n",N);
    return;
  }
}

//動的割り当てを開放.
void freeN(struct node_r *root){
  if(root==NULL){
    free(root);
    return;
  }

  freeN(root->left);
  freeN(root->right);

  free(root);
}

int main(void){
  struct node_r *root=NULL;
  int n=0;

  getNum();

  for(int i=0;i<100;i++){
    root=addN(root,read[i]);
  }

  //printf("%d\n",root->num);

  pushN(root);

  for(int i=0;i<count;i++){
    printf("%d, ",push[i]);
  }
  printf("\n%d個のノードがある.\n\n",count);

  while(1){
    printf("探索する整数(0以下で終了): ");
    scanf("%d",&n);

    if(n<=0){
      printf("探索終了.\n");
      break;
    }
    search(root,n);
  }

  freeN(root);

  return 0;
}
