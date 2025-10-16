package jp.leaningdesign.javastudy;

public class CommonMultiple {

	public static void main(String[] args) {
		// TODO 自動生成されたメソッド・スタブ
		int i = 1;
		while (i < 100) {
			if ((i % 2 == 0) && (i % 3 == 0)) {//論理積
				System.out.println(i);
			}
			i++;//インクリメント演算子
		}

	}

}
