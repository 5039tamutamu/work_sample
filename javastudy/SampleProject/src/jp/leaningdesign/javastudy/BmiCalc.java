package jp.leaningdesign.javastudy;

public class BmiCalc {
/*	BMI(体格指数)を計算するプログラム
 * BMI = 体重 / (身長 * 身長)
 * 体重 kg, 身長 m
 */
	public static void main(String[] args) {
		// TODO 自動生成されたメソッド・スタブ
		double weight, hight, bmi;
		
		weight = 60;
		hight = 176;
		
		//hight = hight / 100;
		hight /= 100;
		
		bmi = weight / (hight * hight);
		
		System.out.println(bmi);
		
		if(bmi < 18.5) {
			System.out.println("やせ型です。");
		}else if(bmi < 25) {
			System.out.println("標準です。");
		}else {
			System.out.println("肥満型です。");
		}
	}

}
