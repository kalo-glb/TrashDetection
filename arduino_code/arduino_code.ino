#define green_diode 9
#define red_diode 7
#define blue_diode 8

#define missing_green_trash(sig) (!(sig & 2))
#define missing_red_trash(sig) (!(sig & 4))
#define missing_blue_trash(sig) (!(sig & 1))

#define green_box A4
#define blue_box A2
#define yellow_box A1

byte signal = 0;

char * asd = "               ";

void setup()
{
  pinMode(red_diode, OUTPUT);
  pinMode(blue_diode, OUTPUT);
  pinMode(green_diode, OUTPUT);
  
  digitalWrite(red_diode, HIGH);
  digitalWrite(blue_diode, HIGH);
  digitalWrite(green_diode, HIGH);
  
  Serial.begin(9600);
  
  pinMode(green_box, INPUT);
  pinMode(blue_box, INPUT);
  pinMode(yellow_box, INPUT);
}

void loop()
{
  if(Serial.available())
  {
    signal = Serial.read();
  }
  
  if(signal != 7)
  {
    digitalWrite(blue_diode, HIGH);
    if(missing_green_trash(signal) && !(digitalRead(blue_box)))
    {
      digitalWrite(red_diode, HIGH);
      digitalWrite(green_diode, LOW);
    }
    else if(missing_red_trash(signal) && (analogRead(green_box) > 200))
    {
      digitalWrite(red_diode, HIGH);
      digitalWrite(green_diode, LOW);
    }
    else if(missing_blue_trash(signal) && !(digitalRead(yellow_box)))
    {
      digitalWrite(red_diode, HIGH);
      digitalWrite(green_diode, LOW);
    }
    else if(digitalRead(blue_box) || 
      (analogRead(green_box) > 200) || 
      digitalRead(yellow_box))
    {
      digitalWrite(green_diode, HIGH);
      digitalWrite(red_diode, LOW);
    }
    
  }
  else
  {
    digitalWrite(red_diode, HIGH);
    digitalWrite(blue_diode, LOW);
    digitalWrite(green_diode, HIGH);
  }
  //sprintf(asd,"%d %d %d", (digitalRead(blue_box)), (digitalRead(yellow_box)), analogRead(green_box));
  /*Serial.print((digitalRead(blue_box)));
  Serial.print(".....");
  Serial.print((digitalRead(yellow_box)));
  Serial.print(".....");
  Serial.print((analogRead(green_box)));
  Serial.println(asd);
  delay(500);*/
}
