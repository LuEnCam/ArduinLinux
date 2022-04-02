#include "crc_table.h"
#include "testn64.h"

void setup()
{
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

  // This is the A button on the controller
  if (N64_status.data1 & 128) {
    increaseBrightness();
  } else {
    decreaseBrightness();
  }
  analogWrite(ledPin, brightness);

    // Mute Tone unless Z is held down
  if (N64_status.data1 & 32) {
    playTone();
  }

  // DEBUG: print it
  print_N64_status();

  delay(1000);
}
