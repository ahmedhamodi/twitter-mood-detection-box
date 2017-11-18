
const int RED_PIN = 5;
const int GREEN_PIN = 6;
const int BLUE_PIN = 7;

// Info procured from IBM watson
struct IBM{
  String emotion;
  double certainty;
};

// Struct first for testing purposes
struct IBM  first;

void setup() {

  Serial.begin(9600);
  
  pinMode(RED_PIN, OUTPUT);   // Red
  pinMode(GREEN_PIN, OUTPUT);   // Green
  pinMode(BLUE_PIN, OUTPUT);   // Blue

  // Can initialize values here from input given by Brett and Ahmed
  first = {"fear", 0.5566};
  first.emotion = "jOY";
  delay(1000);
    
}

void loop() {
  delay(1000);
  // Handles the colour choice for the first letter of every emotion
  switch(first.emotion[0]){
    // Handles the case for Joy. Outputs a skyish blue
    case 'j': 
    case 'J': digitalWrite(6, HIGH);
              digitalWrite(7, HIGH);
              delay(1000);
              first.emotion = "dx";
              digitalWrite(6, LOW);
              digitalWrite(7, LOW);
              break;
    // Handles the case for Disgust. Outputs green
    case 'd': 
    case 'D': digitalWrite(6, HIGH);
              delay(1000);
              first.emotion = "fx";
              digitalWrite(6, LOW);
              break;
    // Handles the case for Fear. Outputs purple
    case 'f': 
    case 'F': digitalWrite(5, HIGH);
              digitalWrite(7, HIGH);
              delay(1000);
              first.emotion = "ax";
              digitalWrite(5, LOW);
              digitalWrite(7, LOW);
              break;
    
    // Handles the case for Anger. Outputs Red      
    case 'a': 
    case 'A': digitalWrite(5, HIGH);
              delay(1000);
              first.emotion = "Sx";
              digitalWrite(5, LOW);
              //first.emotion = "jx";
              break;

    // Handles the case for Sadness. Outputs Blue
    case 's': 
    case 'S': digitalWrite(7, HIGH);
              delay(1000);
              first.emotion = "gx";
              digitalWrite(7, LOW);
              break;

    // Handles the default case. Outputs white
    default: digitalWrite(5, HIGH);
             digitalWrite(6, HIGH);
             digitalWrite(7, HIGH);
             delay(1000);
             first.emotion = "jx";
             digitalWrite(5, LOW);
             digitalWrite(6, LOW);
             digitalWrite(7, LOW);
             break;
  }
}
