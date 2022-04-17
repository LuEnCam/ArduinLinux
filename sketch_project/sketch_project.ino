#include <Arduino.h>
#include <math.h>

#define num_type float

#define SPTR_SIZE   20
char   *sPtr [SPTR_SIZE];
String command;

num_type gl_h;
num_type gl_s;
const num_type gl_v = 1.0;

//LED Pins
const int R_PIN_D = 3;
const int G_PIN_D = 5;
const int B_PIN_D = 6;
//Put GND in GND

int global_mode = 1; // 1 = joystick | 2 = python

//Joystick pins
const int SW_PIN_D = 7;
const int X_AXIS_A = A4;
const int Y_AXIS_A = A5;
//Put GND in GND 
//Put 5V in 5V

bool SWLastState = false;
bool isLEDOn = false;

void setup() {
    pinMode(R_PIN_D, OUTPUT);
    pinMode(G_PIN_D, OUTPUT);
    pinMode(B_PIN_D, OUTPUT);

    pinMode(SW_PIN_D, INPUT_PULLUP);
    pinMode(X_AXIS_A, INPUT);
    pinMode(Y_AXIS_A, INPUT);

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

// Used to split the command received in parameter
int separate (
    String str,
    char   **p,
    int    size )
{
    int  n;
    char s [100];

    strcpy (s, str.c_str ());

    *p++ = strtok (s, " ");
    for (n = 1; NULL != (*p++ = strtok (NULL, " ")); n++)
        if (size == n)
            break;

    return n;
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


void getHSV(num_type x, num_type y, num_type* h, num_type* s, num_type* v) {
  // center is P(511, 511), min-max is (0, 1023)
  x -= 512;
  y -= 512;
  // now center is P(0, 0), min-max is (-512, 511)

  // hue is the angle between 0 and 360 between our position and the xAxis
  num_type hue;
  if (x == 0) {
    if (y == 0)
      hue = 0.0;
    else {
      hue = (y > 0) ? 90.0 : 270.0;
    }
  }

  else {
    hue = atan(y / x) * 180.0 / PI;
    
    // first and third quarter
    if (hue >= 0) {
      // first quarter
      if (x > 0)
      {}
      // third quarter
      else
        hue += 180.0;
    }

    // second and fourth quarter
    else {
      // second quarter
      if (y >= 0)
        hue += 180.0;
      // fourth quarter
      else
        hue += 360.0;
    }
  }

  // saturation = norm(P, joy.pos)
  num_type un = x*x + y*y;
  num_type deux = sqrt(un);
  num_type saturation = deux / 512.0;
  // because sometimes it goes over 1, certainly because the values are even and not odd
  if (saturation > 1)
    saturation = 1;
  // it shouldnt come here
  if (saturation < 0)
    saturation = 0;

  // value hardcoded, might take if from an other input later
  num_type value = 1.0;
  
  *h = hue;
  *s = saturation;
  *v = value;
}

// void debug(num_type h, num_type s, num_type v, num_type un, num_type deux, num_type trois, num_type c, num_type x, num_type m) {
//     Serial.print("hsv: ");
//   Serial.print(h);
//   Serial.print(" ");
//   Serial.print(s);
//   Serial.print(" ");
//   Serial.println(v);

//   Serial.print("123: ");
//   Serial.print(un);
//   Serial.print(" ");
//   Serial.print(deux);
//   Serial.print(" ");
//   Serial.println(trois);
  
//   Serial.print("cxm ");
//   Serial.print(c);
//   Serial.print(" ");
//   Serial.print(x);
//   Serial.print(" ");
//   Serial.println(m);

//   Serial.println();
// }

num_type num_type_mod(num_type x, int mod) {
  while (x > mod)
    x -= mod;
  return x;
}

void getRGBValues(joystick joy, int* r, int* g, int* b) {
  // xAxis and yAxis between 0 and 1023
  // r, g, b between 0 and 255
  num_type h, s, v;
  if (global_mode == 1)
    getHSV(joy.xAxis, joy.yAxis, &h, &s, &v);
  else{
    h = gl_h;
    s = gl_s;
    v = gl_v;
  }

  num_type c = v * s;
  num_type un = h / 60;
  num_type deux = num_type_mod(un, 2) - 1;
  num_type trois = 1 - abs(deux);

  num_type x = c * trois;
  // num_type x = c * (1 - abs(((int)(h / 60.0)) % 2 - 1));
  num_type m = v - c;

  // debug(h, s, v, un, deux, trois, c, x, m);

  num_type num_typeR;
  num_type num_typeG;
  num_type num_typeB;


  if (0 <= h && h < 60) {
    // rgb = [c, x, 0]
    num_typeR = c;
    num_typeG = x;
    num_typeB = 0;
  } else if (60 <= h && h < 120) {
    // rgb = [x, c, 0]
    num_typeR = x;
    num_typeG = c;
    num_typeB = 0;
  } else if (120 <= h && h < 180) {
    // rgb = [0, c, x]
    num_typeR = 0;
    num_typeG = c;
    num_typeB = x;
  } else if (180 <= h && h < 240) {
    // rgb = [0, x, c]
    num_typeR = 0;
    num_typeG = x;
    num_typeB = c;
  } else if (240 <= h && h < 300) {
    // rgb = [x, 0, c]
    num_typeR = x;
    num_typeG = 0;
    num_typeB = c;
  } else if (300 <= h && h < 360) {
    // rgb = [c, 0, x]
    num_typeR = c;
    num_typeG = 0;
    num_typeB = x;
  }

  // Serial.print("rgb1: ");
  // Serial.print(*r);
  // Serial.print(" ");
  // Serial.print(*g);
  // Serial.print(" ");
  // Serial.println(*b);
  *r = (num_typeR + m) * 255;
  *g = (num_typeG + m) * 255;
  *b = (num_typeB + m) * 255;
  // Serial.print("rgb2: ");
  // Serial.print(*r);
  // Serial.print(" ");
  // Serial.print(*g);
  // Serial.print(" ");
  // Serial.println(*b);
  // Serial.println();
}

void globalMode(){
  if (Serial.available()) {
      ///Getting the inputs
    command = Serial.readStringUntil('\n');
    command.trim();
    //The command is received in the following form:
      //1 32.0 1.0 mode
    int N = separate(command, sPtr, SPTR_SIZE);
    isLEDOn = atoi(sPtr[0]);      
    gl_h = atof(sPtr[1]);
    gl_s = atof(sPtr[2]);
    global_mode = atof(sPtr[3]);

    joystick joy = joystick{0,0,0};
    int r, g, b;
    if (isLEDOn)
      getRGBValues(joy, &r, &g, &b);
    toggleLED(isLEDOn, r, g, b);
  }
}

void check_mode(){
    if (Serial.available()) {
      ///Getting the inputs
      command = Serial.readStringUntil('\n');
      command.trim();
      //The command is received in the following form:
      //1 32.0 1.0 mode
      int N = separate(command, sPtr, SPTR_SIZE);
      isLEDOn = atoi(sPtr[0]);      
      gl_h = atof(sPtr[1]);
      gl_s = atof(sPtr[2]);
      global_mode = atof(sPtr[3]);
  }     
}

void loop() {
  if (global_mode == 2){
    globalMode();
    delay(10);
  }
  else {
    joystick joy = getJoystick();
    if (!joy.isPush)
      SWLastState = false;
  
    // the button just got clicked (simulate a switch)
    else if (joy.isPush != SWLastState) {
      SWLastState = true;
      isLEDOn = !isLEDOn;
    }
      
    int r, g, b;
    if (isLEDOn)
      getRGBValues(joy, &r, &g, &b);
    toggleLED(isLEDOn, r, g, b);
  
    check_mode();
    
    delay(10);
  } 
}
