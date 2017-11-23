// Pins for output to RGB LED
const int RED_PIN = 5;
const int GREEN_PIN = 4;
const int BLUE_PIN = 3;

struct rgb{
	int r;
	int g;
	int b;
};

// Get sign of a number
int sign(int x) {
    return (x > 0) - (x < 0);
}

// Scales intensity of rgb value by a scalar
struct rgb scale(struct rgb colour, double scalar) {
	colour.r = (int)((double)colour.r*scalar);
	colour.g = (int)((double)colour.g*scalar);
	colour.b = (int)((double)colour.b*scalar);
	return colour;
}

// Displays rgb colour on LED
void draw_PWM(struct rgb colour) {
	analogWrite(RED_PIN, colour.r);
	analogWrite(GREEN_PIN, colour.g);
	analogWrite(BLUE_PIN, colour.b);
}

// Transitions smoothly between two colours over length (ms)
void transition(struct rgb colour, struct rgb new_colour, int iters, int length) {
	struct rgb intermediate = colour;
	double rstep = (new_colour.r - colour.r)/(double)iters;
	double gstep = (new_colour.g - colour.g)/(double)iters;
	double bstep = (new_colour.b - colour.b)/(double)iters;
	int delay_time = length/iters;
	for(int i=0; i < iters; i++) {
		intermediate.r = (int) (colour.r + rstep*i);
		intermediate.g = (int) (colour.g + gstep*i);
		intermediate.b = (int) (colour.b + bstep*i);
		draw_PWM(intermediate);
		delay(delay_time);
	}
	draw_PWM(new_colour);
}

// Initialise variables
int incomingByte = 'x';
double confidence = 1;
int breath = 1; // Used to create 'breathing' light effect
struct rgb colour = {255, 255, 255};
struct rgb new_colour;

void setup() {
	Serial.begin(9600);
	pinMode(RED_PIN, OUTPUT);
	pinMode(GREEN_PIN, OUTPUT);
	pinMode(BLUE_PIN, OUTPUT);		
}

void loop() {
	
	// Oscillates intensity slightly for 'breathing' effect
	confidence += breath*0.25;
	breath *= -1;
	if(confidence > 1) {
		confidence = 1;
	}
	if(confidence <= 0) {
		confidence = 0.1;
	}

	// Get emotion and confidence data from serial
	if (Serial.available() > 0) {
		incomingByte = Serial.read();
		confidence = Serial.parseFloat();
	}

	// Display colour
	switch(incomingByte){
		// Handles the case for Joy. Outputs yellow
		case 'j': 
		case 'J':
			new_colour = {255, 48, 0};
			new_colour = scale(new_colour, confidence);
			break;
		// Handles the case for Disgust. Outputs green
		case 'd': 
		case 'D':
			new_colour = {0, 255, 0};
			new_colour = scale(new_colour, confidence);
			break;
		// Handles the case for Fear. Outputs purple
		case 'f': 
		case 'F':
			new_colour = {255, 0, 255};
			new_colour = scale(new_colour, confidence);
			break;
		// Handles the case for Anger. Outputs Red      
		case 'a': 
		case 'A':
			new_colour = {255, 0, 0};
			new_colour = scale(new_colour, confidence);
			break;
		// Handles the case for Sadness. Outputs Blue
		case 's': 
		case 'S':
			new_colour = {0, 0, 255};
			new_colour = scale(new_colour, confidence);
			break;
		// Handles the default case. Outputs white
		default:
			new_colour = {255, 255, 255};
			new_colour = scale(new_colour, confidence);
			break;
	}
	transition(colour, new_colour, 500, 1000);
	colour = new_colour;
}
