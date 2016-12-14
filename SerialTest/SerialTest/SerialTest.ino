#include <Servo.h>
Servo servo;
const int HOL1 = 9;  // DIGITAL 5番ピンにHOLと名前を付ける。（ホールド）大きい方
const int DIR1= 10;  // DIGITAL 4番ピンにDIRと名前を付ける。（回転方向）　
const int PUL1 = 11;  // DIGITAL 3番ピンにPULと名前を付ける。（パルス）　
const int HOL2 = 3;  // DIGITAL 5番ピンにHOLと名前を付ける。（ホールド）小さい方
const int DIR2 = 4;  // DIGITAL 4番ピンにDIRと名前を付ける。（回転方向）　
const int PUL2 = 5;  // DIGITAL 3番ピンにPULと名前を付ける。（パルス）
const int waitTime = 8000; //スピードは大きいほどゆっくり
void setup() {
  // put your setup code here, to run once:
  pinMode(HOL1, OUTPUT); // HOLピンを出力に設定
  pinMode(DIR1, OUTPUT); // DIRピンを出力に設定
  pinMode(PUL1, OUTPUT); // PULピンを出力に設定
  pinMode(HOL2, OUTPUT); // HOLピンを出力に設定
  pinMode(DIR2, OUTPUT); // DIRピンを出力に設定
  pinMode(PUL2, OUTPUT); // PULピンを出力に設定
  servo.attach(13); //サーボモーターつけたとこ
  servo.write(0);
  delay(1000);
  Serial.begin(9600);
}


void loop() {
  // put your main code here, to run repeatedly: 
  int cnt_buf;
  int inputchar;
  // シリアルポートより1文字読み込む
  inputchar = Serial.read();
  if(inputchar != -1){
    delay(100);
//    cnt_buf = Serial.available();  //受信文字数
//    char charA_out[cnt_buf+1];
//    for (int iii = 0; iii < cnt_buf; iii++){
//      charA_out[iii] = Serial.read();
//    }
//    charA_out[cnt_buf] = '\0';  //終端文字
//     
//    Serial.println(charA_out[0]);
//     読み込んだデータが -1 以外の場合　以下の処理を行う 
    
    switch ('c'){ 
      case 'a':
        Serial.println("a");
        largeMove(185,0);
        servo.write(150);
        delay(1000);
        largeMove(185,1);
        servo.write(0);
        break;
      case 'b':
        Serial.println("b");
        largeMove(185,0);
        smallMove(130,0);
        servo.write(150);
        delay(1000);
        smallMove(130,1);
        largeMove(185,1);
        servo.write(0);
        break;
      case 'c':
        Serial.println("c");
        largeMove(90,0);
        smallMove(130,0);
        servo.write(150);
        delay(1000);
        smallMove(130,1);
        largeMove(90,1);
        servo.write(0);
        break;
       case 'd':
        Serial.println("d");
        largeMove(90,0);
        servo.write(150);
        delay(1000);
        largeMove(90,1);
        servo.write(0);
        break;
    }
    finish();
  }  
}

void largeMove(int runTime,int vector){ //vector 0で正方向、1で逆方向
  digitalWrite(HOL1, HIGH); // HOLをHIGH(1)にする。1: ON
  if(vector == 0){
      digitalWrite(DIR1, HIGH); // DIRをHIGH(1)にする。1: CCW
    }else{
      digitalWrite(DIR1, LOW); // DIRをHIGH(1)にする。1: CCW
    }
  for( int i = 1 ; i <= runTime ; i++ ){
    digitalWrite(PUL1, HIGH); // PULをHIGH(1)にする。1: 5 V
    delayMicroseconds(waitTime); 
    digitalWrite(PUL1, LOW);  // PULをLOW(0)にする。 0: 0V
    delayMicroseconds(waitTime);   // 待機
     }
}

void smallMove(int runTime,int vector){
  digitalWrite(HOL2, HIGH); // HOLをHIGH(1)にする。1: ON
  if(vector == 0){
      digitalWrite(DIR2, HIGH); // DIRをHIGH(1)にする。1: CCW
    }else{
      digitalWrite(DIR2, LOW); // DIRをHIGH(1)にする。1: CCW
    }
  
  for( int i = 1 ; i <= runTime ; i++ ){
    digitalWrite(PUL2, HIGH); // PULをHIGH(1)にする。1: 5 V
    delayMicroseconds(waitTime); 
    digitalWrite(PUL2, LOW);  // PULをLOW(0)にする。 0: 0V
    delayMicroseconds(waitTime);   // 待機
     }
}

void finish(){
  digitalWrite(HOL1, LOW); // HOLをLOW(0)にする。0: OFF(0 V)
  digitalWrite(DIR1, LOW); // DIRをLOW(0)にする。0: CW(0 V)
  digitalWrite(PUL1, LOW); // PULをLOW(0)にする。0: 0 V
  
  digitalWrite(HOL2, LOW); // HOLをLOW(0)にする。0: OFF(0 V)
  digitalWrite(DIR2, LOW); // DIRをLOW(0)にする。0: CW(0 V)
  digitalWrite(PUL2, LOW); // PULをLOW(0)にする。0: 0 V

  while(1);               // 無限ループで強制ストップ
}
