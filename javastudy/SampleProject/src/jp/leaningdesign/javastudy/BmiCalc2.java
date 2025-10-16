package jp.leaningdesign.javastudy;

import java.util.Scanner;


public class BmiCalc2 {
/*	BMI(体格指数)を計算するプログラム
 * BMI = 体重 / (身長 * 身長)
 * 体重 kg, 身長 m
 */
	public static void main(String[] args) {
		// TODO 自動生成されたメソッド・スタブ
		double weight, hight, bmi;
		
		//weight = 60;
		//hight = 176;
		
		Scanner stdIn = new Scanner(System.in);
		System.out.println("体重は？(kg):");
		weight = stdIn.nextDouble();
		System.out.println("身長は？(cm):");
		hight = stdIn.nextDouble();
		
		hight /= 100;
		
		bmi = weight / (hight * hight);
		
		System.out.println("BMI: " + bmi + "です。");
		
		if(bmi < 18.5) {
			System.out.println("やせ型です。");
		}else if(bmi < 25) {
			System.out.println("標準です。");
		}else {
			System.out.println("肥満型です。");
		}
	}

}
