
int red_blink = 0;
int green_blink = 0;
int yellow_blink = 0;
int blue_blink = 0;
int full_blink=0;

void setup() {
  // put your setup code here, to run once:
 // // configure LEDs interface
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT); //jaune
  pinMode(7, OUTPUT); // bleu
  pinMode(9, OUTPUT); //rouge
  // push buttons
  pinMode(3, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP); //rouge ?

  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  digitalWrite(2, 0);
  digitalWrite(4, 0);
  digitalWrite(7, 0);
  digitalWrite(9, 0);
}

void switch_off() {
    digitalWrite(2, 0);
  digitalWrite(4, 0);
  digitalWrite(7, 0);
  digitalWrite(9, 0);
  red_blink= 0;
  green_blink= 0;
  blue_blink= 0;
  yellow_blink= 0;
  full_blink=0;
}


void blink_full() {
  digitalWrite(9, 1);
  digitalWrite(7, 0);
  digitalWrite(4, 0);
  digitalWrite(2, 0);
  delay(100);
  digitalWrite(9, 0);
  digitalWrite(7, 1);
  digitalWrite(4, 0);
  digitalWrite(2, 0);
  delay(100);
  digitalWrite(9, 0);
  digitalWrite(7, 0);
  digitalWrite(4, 1);
  digitalWrite(2, 0);
  delay(100);
  digitalWrite(9, 0);
  digitalWrite(7, 0);
  digitalWrite(4, 0);
  digitalWrite(2, 1);
  delay(100);
}

void blink_red() {
  digitalWrite(9, 1);
  delay(400);
  digitalWrite(9, 0);
}

void blink_blue() {
  digitalWrite(7, 1);
  delay(400);
  digitalWrite(7, 0);
}

void blink_yellow() {
  digitalWrite(4, 1);
  delay(400);
  digitalWrite(4, 0);
}

void blink_green() {
  digitalWrite(2, 1);
  delay(400);
  digitalWrite(2, 0);
}

void button_loop() {
      int rouge = 1;
      int bleu = 1;
      int jaune = 1;
      int vert =1;
       rouge = digitalRead(8);
       delay(100);
       bleu = digitalRead(6);
       delay(100);
       jaune = digitalRead(3);
       delay(100);
       vert = digitalRead(5);
      delay(100);

      if (rouge == LOW) {
       Serial.write("rouge\n");
      }
      if (bleu == LOW) {
        Serial.write("bleu\n");
      }
      if (vert == LOW) {
       Serial.write("vert\n");
      } 
      if (jaune == LOW) {
       Serial.write("jaune\n");
     }
}

void loop() {

  int incomingByte = 0;

     if (Serial.available() > 0) {
     // read the incoming byte:
      incomingByte = Serial.read();
      if (incomingByte == 'a') {
        green_blink=1;
      } else if (incomingByte == 's') {
        switch_off();
      } else if (incomingByte == 'b') {
        full_blink=1;
      } else {
        // nothing
      }
     }
    if (full_blink == 1) {
      blink_full();
    }
     if (green_blink == 1) {
      blink_green();
     }

    if (blue_blink == 1) {
      blink_blue();
    }
    if (red_blink == 1) {
      blink_red();
    }
    if (yellow_blink == 1) {
      blink_yellow();
    }

     button_loop();

  
  
}
