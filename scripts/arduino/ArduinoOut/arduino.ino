
const int RED_PIN = 5;
const int GREEN_PIN = 6;
const int BLUE_PIN = 7;

struct IBM{
  String emotion;
  double certainty;
};

struct IBM  first;

void setup() {

  Serial.begin(9600);
  
  pinMode(RED_PIN, OUTPUT);   // Red
  pinMode(GREEN_PIN, OUTPUT);   // Green
  pinMode(BLUE_PIN, OUTPUT);   // Blue

  
  first = {"fear", 0.5566};
  first.emotion = "JOY";
  delay(1000);
  //Serial.println("fear");
    
}

void loop() {
  delay(1000);
  Serial.println(first.emotion);
  Serial.println(first.certainty);
 
}
