#include <math.h>

//LED Pins
const int R_PIN_D = 3;
const int G_PIN_D = 5;
const int B_PIN_D = 6;
//Put GND in GND


//Joystick pins
const int SW_PIN_D = 7;
const int X_AXIS_A = A4;
const int Y_AXIS_A = A5;
//Put GND in GND 
//Put 5V in 5V


//Rotator pins
const int CLK = 10; //check rotation
const int DT = 11; // rotator direction
//Put GND in GND 
//Put 5V in 5V

bool SWLastState = false;
bool isLEDOn = false;

int value;
int rotation;
int rotationValue = 0;
const int maxRotation = 19;
int maintainedValue = 0; //max to 10 then decrease. Depending on rotation value
int clockwise = 1;

int getPosRotation(int _DTRead)
{
  if (value != rotation)
  {
    

    if (_DTRead != value ) //sens aiguille montre.
      clockwise = 1;
    else
      clockwise = -1;

    rotationValue += clockwise;

    rotationValue = rotationValue % maxRotation ;

    if (rotationValue < 10)
      maintainedValue += 1;
    else
      maintainedValue -= 1;   

    Serial.println("rotation ");
    Serial.println(maintainedValue);
  }
  
}

void setup() {
    pinMode(R_PIN_D, OUTPUT);
    pinMode(G_PIN_D, OUTPUT);
    pinMode(B_PIN_D, OUTPUT);

    pinMode(SW_PIN_D, INPUT_PULLUP);
    pinMode(X_AXIS_A, INPUT);
    pinMode(Y_AXIS_A, INPUT);

    pinMode (CLK,INPUT);
    pinMode (DT,INPUT);

    rotation = digitalRead(CLK); //Init rotation

    Serial.begin(9600);
}

struct joystick {
  bool isPush;
  int xAxis;
  int yAxis;
};

struct joystick getJoystick() {
  return joystick {
    !digitalRead(SW_PIN_D),
    analogRead(X_AXIS_A),
    analogRead(Y_AXIS_A)
    };
}

void toggleLED(bool joy, int r, int g, int b) {
    // turn on the led
    if (joy) {
      analogWrite(R_PIN_D, r);
      analogWrite(G_PIN_D, g);
      analogWrite(B_PIN_D, b);
    }
    // turn off the led
    else {
      analogWrite(R_PIN_D, LOW);
      analogWrite(G_PIN_D, LOW);
      analogWrite(B_PIN_D, LOW);
    }
}

// https://arduino-and-atmel-projects.webnode.sk/l/hsv-to-rgb-model/

void hsv_to_rgb(uint16_t h, uint32_t s, uint32_t v, int* outR, int* outG, int* outB)
{
    
    if (h>=36000) h-=36000;
    int16_t ph = h/6;  
    ph=ph % 2000;
    ph-=1000;
    ph=1000-abs(ph);
    if (h==0)
        ph=0;
    uint32_t c= v*s;
    uint32_t x2 = c*ph;
    uint8_t x=x2/255000;
    uint8_t r,g,b;
    int32_t m=v*(255-s)/255;
    x+=m;
    if ( 0<=h && h<6000 )       {  r=v;g=x;b=m;}        //rgb = [c, x, 0];
    if ( 6000<=h && h<12000 )   {  r=x;g=v;b=m;}        //rgb = [x, c, 0];
    if ( 12000<=h && h<18000 )  {  r=m;g=v;b=x;}        //rgb = [0, c, x];
    if ( 18000<=h && h<24000 )  {  r=m;g=x;b=v;}        //rgb = [0, x, c];
    if ( 24000<=h && h<30000 )  {  r=x;g=m;b=v;}        //rgb = [x, 0, c];
    if ( 30000<=h && h<36000 )  {  r=v;g=m;b=x;}        //rgb = [c, 0, x];
    //uint16_t rgb = (((r&0b11111000)<<8)|((g&0b11111100)<<3)|(b>>3));
    *outR = r;
    *outG = g;
    *outB = b;
}

void getRGBValues(joystick joy, int* r, int* g, int* b) {
  // xAxis and yAxis between 0 and 1023
  // r, g, b between 0 and 255

  // we use hsv color model, the joystick allows to change the HUE and Saturation
  // another molette (KY040) allows to change the value (intensity of the light)
  // https://en.wikipedia.org/wiki/HSL_and_HSV
  // https://www.lifewire.com/what-is-hsv-in-design-1078068

  // center is P(512; 512);

  int xVector = joy.xAxis - 512;
  int yVector = joy.yAxis - 512;
  
  // saturation = norme (P, joy.pos)
  uint16_t saturation = sqrt(square(xVector) + square(yVector));

  // Hue is the angle between 0 and 360 between our position and the xAxis)
  // simple math, use pythagore and tan the y on x
  // if x == 0 => either 90° or 270°
  uint16_t hue;
  if (xVector == 0) {
    hue = yVector >= 0 ? 90 : 270;
  } else {
    hue = atan(yVector/xVector);
  }

  // value is given by the MOLETTE
  uint16_t value = 127; // TODO: hardcoded

  hsv_to_rgb(hue, saturation, value, r, g, b);

  /*
  Serial.print("r = ");
  Serial.println(*r);
  Serial.print("g = ");
  Serial.println(*g);
  Serial.print("b = ");
  Serial.println(*b);
  Serial.println();
  */
  // TODO: formule surement fausse, valeurs etranges (24->140, pas plus pas moins)
}

void loop() {
  
  value = digitalRead(CLK); //Checks if rotation

  getPosRotation(digitalRead(DT));

  rotation = value;

  joystick joy = getJoystick();
  
  if (!joy.isPush)
    SWLastState = false;

  // the button just got clicked (simulate a switch)
  else if (joy.isPush != SWLastState) {
    SWLastState = true;
    isLEDOn = !isLEDOn;
  }
  
  int r, g, b;
  getRGBValues(joy, &r, &g, &b);
  toggleLED(isLEDOn, r, g, b);

  
  //delay(100);
  
}
