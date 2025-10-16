///////////////////////////////////////////////////////////////////////
//以下の2点を行うプログラムです．
//・Arduinoのアナログピンからミリ単位で正確にデータロギングを行う
//・ArduinoからPCへデータを送信する
//
//PCとのシリアル通信を前提としています．
//使用したい場合はpython側のコードも一緒に確認してみてください．
//・PCから開始シグナルを受信しないとロギングを開始しません．
//・PC側でデータを受信・復元する必要があります．
//////////////////////////////////////////////////////////////////////

unsigned long period = 1000;  //計測間隔(microsec)

int R;  //開始コマンド受信用

int A = 0;  //アナログデータ一時保存
int B = 0;
int C = 0;
byte data[7]; //送信データ配列

unsigned long t0; //開始時刻
unsigned long t;  //t0からの経過時間
unsigned long counter;

//Arduinoの起動のたび一度だけ実行される
void setup() {
  //8bit*13byte*1000Hz=104000bps以上
  Serial.begin(115200);
  data[0] = (byte) 128;
}

//setup()実行後無限にループする(本コードでは実際のループはLogging()で行う)
void loop() {
  Wait();
  Reset();
  Logging();
}

void Wait() { //開始シグナルを受信するまで待機
  while (Serial.available() == 0) {
    delay(10);
  }
  R = Serial.read();
}

void Reset() { //時間関係の変数の初期化
  counter = period;
  t0 = micros();
}

void Logging() {  //一定間隔でデータロギングと送信を実行(必ずReset()の後ろ)
  while(1) {
    if (micros() - t0 >= counter) { //次の計測時間まで待機
      
      //アナログピンからデータを10bitで読み取り
      A = analogRead(0);
      B = analogRead(1);
      C = analogRead(2);

      //シリアル通信は8bitなので，データを上下7bitに分割
      data[1] = (A >> 7) & 127;
      data[2] = A & 127;
      data[3] = (B >> 7) & 127;
      data[4] = B & 127;
      data[5] = (C >> 7) & 127;
      data[6] = C & 127;

      Serial.write(data, 7);//シリアル送信
      
      counter += period;
    }
  }
}
