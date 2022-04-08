#include "crc_table.h"
#include "testn64.h"

//LED Pins
const int R_PIN_D = 3;
const int G_PIN_D = 5;
const int B_PIN_D = 6;
//Put GND in GND

bool SWLastState = false;
bool isLEDOn = false;

uint16_t g_value = 255;  
int g_hue = 0;
float g_saturation = 1.0;

void setup()
{
  pinMode(R_PIN_D, OUTPUT);
  pinMode(G_PIN_D, OUTPUT);
  pinMode(B_PIN_D, OUTPUT);
  
  Serial.begin(9600);

  // Communication with gamecube controller on this pin
  // Don't remove these lines, we don't want to push +5V to the controller
  digitalWrite(N64_PIN, LOW);
  pinMode(N64_PIN, INPUT);

  // Initialize the gamecube controller by sending it a null byte.
  // This is unnecessary for a standard controller, but is required for the
  // Wavebird.
  unsigned char initialize = 0x00;
  noInterrupts();
  N64_send(&initialize, 1);

  // Stupid routine to wait for the gamecube controller to stop
  // sending its response. We don't care what it is, but we
  // can't start asking for status if it's still responding
  int x;
  for (x=0; x<64; x++) {
      // make sure the line is idle for 64 iterations, should
      // be plenty.
      if (!N64_QUERY)
          x = 0;
  }

  // Query for the gamecube controller's status. We do this
  // to get the 0 point for the control stick.
  unsigned char command[] = {0x01};
  N64_send(command, 1);
  // read in data and dump it to N64_raw_dump
  N64_get();
  interrupts();
  translate_raw_data();
}

void update_g_value(uint16_t i){
  g_value = g_value + i;
  //Serial.println(g_value);
}

void update_g_saturation(float i){
  g_saturation = g_saturation + i;
  //Serial.println(g_value);
}

void toggleLED(bool isOn, int r, int g, int b) {
    // turn on the led
    if (isOn) {
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
void hsv_to_rgb(int h, float s, uint32_t v, int* outR, int* outG, int* outB)
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

void n64_get_angle(int x, int y){
  
  int xmin = -80;
  int ymin = -80;
  
  int xmax = 79;
  int ymax = 79;
  
  float val = 0;
  
  val = x != 0 ? atan((float)y / (float)x) : acos(2);
  //Serial.print("val 1 ");
  //Serial.println(val);
  

    val = (float)val / (float)PI * 180.0;
    //Serial.print("val 3 ");
    //Serial.println(val); 
    val += 90.0;
    //Serial.print("val 4 ");
    //Serial.println(val); 
    val = x >= 0 ? val : val + 180.0;
    //Serial.print("val 5 ");
    //Serial.println(val); 

    g_hue = (int)val;

}

void getRGBValues(unsigned char _data1, unsigned char _data2, char _stick_x, char _stick_y ,int* r, int* g, int* b) {
  // xAxis and yAxis between 0 and 1023
  // r, g, b between 0 and 255

  // we use hsv color model, the joystick allows to change the HUE and Saturation
  // another molette (KY040) allows to change the value (intensity of the light)
  // https://en.wikipedia.org/wiki/HSL_and_HSV
  // https://www.lifewire.com/what-is-hsv-in-design-1078068

  // center is P(512; 512);

  /////////////int xVector = joy.xAxis - 512;
  /////////////int yVector = joy.yAxis - 512;
  int xVector = _stick_x;
  int yVector = _stick_y;

  // now center is P(0; 0), min-max is (-80, 80)

  // saturation = norme(P, joy.pos)
  //uint16_t saturation = sqrt(square(xVector) + square(yVector)) * 100;
  float saturation = g_saturation;


  // Hue is the angle between 0 and 360 between our position and the xAxis)
  // simple math, use pythagore and tan the y on x
  // if x == 0 => either 90° or 270°
  uint16_t hue;

  if (xVector == 0) {
    hue = yVector >= 0 ? 9000 : 27000;
  } 
  else 
  {
    double ratio = yVector/(double)xVector;
    // double alpha = atan(ratio) * 180 / PI * 1000;
    double alpha = atan(ratio);
    //Serial.println(alpha);
    
    n64_get_angle(xVector,yVector);
    hue = g_hue;
    Serial.println(hue);
    Serial.println(g_saturation);
    /*
    // first and third quarter
    if (alpha >= 0) 
    {
      // first quarter
      if (xVector >= 0) 
      {
        hue = alpha;
      }
      // third quarter
      else 
      {
        hue = alpha + 18000;
      }
    }
    // second and fourth quarter
    else 
    {
      // second quarter
      if (yVector >= 0) 
      {
        hue = alpha + 18000;
      }
      // fourth quarter
      else 
      {
        hue = alpha + 36000;
      }
    }
      */
  }

  
  //Serial.println(hue/100);

  // uint16_t value = 255; // TODO: hardcoded
  // hsv_to_rgb(hue, saturation, value, r, g, b);
//  HSV_to_RGB_2(hue, g_saturation, g_value);
  setLedColorHSV(hue,g_saturation,g_value);


}

//Convert a given HSV (Hue Saturation Value) to RGB(Red Green Blue) and set the led to the color
//  h is hue value, integer between 0 and 360
//  s is saturation value, double between 0 and 1
//  v is value, double between 0 and 1
//http://splinter.com.au/blog/?p=29
void setLedColorHSV(int h, double s, double v) {
  //this is the algorithm to convert from RGB to HSV
  double r=0; 
  double g=0; 
  double b=0;

  double hf=h/60.0;

  int i=(int)floor(h/60.0);
  double f = h/60.0 - i;
  double pv = v * (1 - s);
  double qv = v * (1 - s*f);
  double tv = v * (1 - s * (1 - f));

  switch (i)
  {
  case 0: //rojo dominante
    r = v;
    g = tv;
    b = pv;
    break;
  case 1: //verde
    r = qv;
    g = v;
    b = pv;
    break;
  case 2: 
    r = pv;
    g = v;
    b = tv;
    break;
  case 3: //azul
    r = pv;
    g = qv;
    b = v;
    break;
  case 4:
    r = tv;
    g = pv;
    b = v;
    break;
  case 5: //rojo
    r = v;
    g = pv;
    b = qv;
    break;
  }

  //set each component to a integer value between 0 and 255
  int red=constrain((int)255*r,0,255);
  int green=constrain((int)255*g,0,255);
  int blue=constrain((int)255*b,0,255);

  setLedColor(red,green,blue);
}

void setLedColor(int red, int green, int blue) {
  
  toggleLED(isLEDOn, red, green, blue);
}

void loop()
{
  int i;
  unsigned char data, addr;

  // Command to send to the gamecube
  // The last bit is rumble, flip it to rumble
  // yes this does need to be inside the loop, the
  // array gets mutilated when it goes through N64_send
  unsigned char command[] = {0x01};

  // don't want interrupts getting in the way
  noInterrupts();
  // send those 3 bytes
  N64_send(command, 1);
  // read in data and dump it to N64_raw_dump
  N64_get();
  // end of time sensitive code
  interrupts();

  // translate the data in N64_raw_dump to something useful
  translate_raw_data();

   //for (i=0; i<16; i++) {
   //  Serial.print(N64_raw_dump[i], DEC);
   //}
  //Serial.print(' ');
  //Serial.print(N64_status.stick_x, DEC);
  //Serial.print(' ');
  //Serial.print(N64_status.stick_y, DEC);
  //Serial.print(" \n");


  if (!(N64_status.data1 & N64_START))
    SWLastState = false;

  // the button just got clicked (simulate a switch)
  else if ((N64_status.data1 & N64_START) != SWLastState) {
    SWLastState = true;
    isLEDOn = !isLEDOn;
  }

  if (N64_status.data1 & N64_DPAD_U)
    update_g_value(20);
  else if (N64_status.data1 & N64_DPAD_D) 
    update_g_value(-20);

  if (N64_status.data1 & N64_DPAD_L)
    update_g_saturation(0.1);
  else if (N64_status.data1 & N64_DPAD_R) 
    update_g_saturation(-0.1);


  int r, g, b;
  if (isLEDOn)
    getRGBValues(N64_status.data1,N64_status.data2,N64_status.stick_x,N64_status.stick_y, &r, &g, &b);
  //toggleLED(isLEDOn, r, g, b);
  //toggleLED(isLEDOn, 255, 0, 0);


  // DEBUG: print it
  //print_N64_status();

  delay(100);
}
