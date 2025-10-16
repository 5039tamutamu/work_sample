#include <stdio.h>
#include <stdlib.h>

struct node {
  int data;
  struct node *left;
  struct node *right;
};

struct node *insert_data(int x, struct node *p)
{
  struct node *nd;
  if (p == NULL) {
    if ((nd = (struct node *)malloc(sizeof(struct node))) == NULL) {
      fprintf(stderr, "Out of memory\n");
      exit(1);
    }
    nd->data = x;
    nd->left = NULL;
    nd->right = NULL;
    return nd;
  }

  if (x == p->data) {
    return p;
  } else if (x < p->data) {
    p->left = insert_data(x, p->left);
    return p;
  } else {
    p->right = insert_data(x, p->right);
    return p;
  }
}

void print_tree(struct node *p)
{
  if (p == NULL) {
    return;
  }

  print_tree(p->left);
  printf("%d\n", p->data);
  print_tree(p->right);
}

int search_tree(int x, struct node *p)
{
  /* Implement by yourself */
}

int count_nodes(struct node *p)
{
  /* Implement by yourself */
}

void free_tree(struct node *p)
{
  if (p == NULL) {
    return;
  } else {
    if (p->left != NULL) {
      free_tree(p->left);
    }
    if (p->right != NULL) {
      free_tree(p->right);
    }
    free(p);
  }
}

int main(int argc, char *argv[])
{
  FILE *fp;
  int i, x;
  struct node *root = NULL;

  if (argc != 2) {
    fprintf(stderr, "Missing file argument\n");
    exit(1);
  }

  if ((fp = fopen(argv[1], "r")) == NULL) {
    fprintf(stderr, "Can't open %s\n", argv[1]);
    exit(1);
  }

  for (i = 0; i < 100; i++) {
    if (fscanf(fp, "%d", &x) != 1) {
      fprintf(stderr, "Can't read data\n");
      exit(1);
    }
    if (x <= 0) {
      fprintf(stderr, "Invalid data: %d\n", x);
      exit(1);
    }
    root = insert_data(x, root);
  }

  fclose(fp);

  print_tree(root);
  printf("%d numbers read\n", count_nodes(root));

  while (1) {
    printf("Input number ");
    if (scanf("%d", &x) == EOF) {
      fprintf(stderr, "Can't read input\n");
      exit(1);
    }
    if (x <= 0) {
      break;
    }
    if (search_tree(x, root) == 1) {
      printf("%d: Found\n", x);
    } else {
      printf("%d: Not found\n", x);
    }
  }

  free_tree(root);

  return 0;
}