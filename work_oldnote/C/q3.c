#include <stdio.h>
int main(void){
  int Score[9], i;
  int unit[9]={5,6,1,1,3,2,2,2,2};
  int GPAsum=0, unitsum=0;
  double GPA;
  char subject[9][100]={"Linear-Algebra", "Inf-theory", "Communication", "Academic-Eng", "Laboratory", "Basic-Physics", "C-language", "Basic-Economics", "Basic-German"};
  
  printf("Input score: ");
  for(i=0; i<9; i++){
    printf("%s score: ", subject[i]);
    scanf("%d", &Score[i]);
  }
  printf("\n");
  printf("Subjectname\t Unit\t Score\t Rank\t\n");

  for(i=0; i<9; i++){
    unitsum+=unit[i];
    printf("%s\t%4d\t%6d\t", subject[i], unit[i], Score[i]);

   if(Score[i]<60){ 
      printf("  F\t\n");
  }else if(Score[i]<70){            
      printf("  C\t\n");
      GPAsum+=unit[i];
  }else if(Score[i]<80){
      printf("  B\t\n", subject[i]);
      GPAsum+=unit[i]*2;
   }else if(Score[i]<90){ 
	printf("  A\t\n");
        GPAsum+=unit[i]*3;
   }else{           
	printf("  A+\t\n");
        GPAsum+=unit[i]*4;
   }
  }

  for(i=0; i<40; i++) printf("-");
  printf("\n");
  GPA=(double)GPAsum/(double)unitsum;
  printf("GPA: %.2f\n", GPA);
  return 0;
  }
 
