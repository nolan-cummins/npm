#include <AccelStepper.h>
#include <MultiStepper.h>
#include <SafeString.h>
#include <ezButton.h>

//
// pin assignments
//

//Enable pin - DON'T MODIFY
#define EN 8

const int MOTOR_X_STEP_PIN = 4;
const int MOTOR_X_DIRECTION_PIN = 7;
const int MOTOR_Y_STEP_PIN = 2;
const int MOTOR_Y_DIRECTION_PIN = 5;
const int MOTOR_Z_STEP_PIN = 3;
const int MOTOR_Z_DIRECTION_PIN = 6; 

//byte incoming;
bool was_w_pressed = false;
bool was_a_pressed = false;
bool was_s_pressed = false;
bool was_d_pressed = false;
bool was_space_pressed = false;
bool was_shift_pressed = false;

// create three stepper motor objects, one for each motor
AccelStepper stepper_x(AccelStepper::DRIVER, MOTOR_X_STEP_PIN, MOTOR_X_DIRECTION_PIN);           // works for a4988 (Bipolar, constant current, step/direction driver)
AccelStepper stepper_y(AccelStepper::DRIVER, MOTOR_Y_STEP_PIN, MOTOR_Y_DIRECTION_PIN);           // works for a4988 (Bipolar, constant current, step/direction driver)
AccelStepper stepper_z(AccelStepper::DRIVER, MOTOR_Z_STEP_PIN, MOTOR_Z_DIRECTION_PIN);           // works for a4988 (Bipolar, constant current, step/direction driver)

// create limit switch objects
ezButton ls_x_beg(23);
ezButton ls_x_end(22);
ezButton ls_y_beg(24);
ezButton ls_y_end(25);
ezButton ls_z_beg(26);
ezButton ls_z_end(27);

float speed;
bool home = false;
bool homing = false;
bool x_beg = false;
bool x_end = false;
bool y_beg = false;
bool y_end = false;
bool z_beg = false;
bool z_end = false;

float max_speed = 100000;
float acceleration = 5000;

float x_ceiling = 30000;
float y_ceiling = 30000;
float z_ceiling = 30000;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 100; // Interval in milliseconds

unsigned long t1 = 0;
unsigned long t2 = 0;

// Multistepper
MultiStepper steppers;
long positions[3] = {0, 0, 0}; // Array of desired stepper positions
long origin[3] = {0, 0, 0};
int lower_limit = 40;

bool K1 = true;
bool K2 = true;
bool K3 = true;
bool K4 = true;

void setup() {
  Serial.begin(9600);
  SafeString::setOutput(Serial); // for SafeString error msgs
  
  pinMode(31, OUTPUT); // IN1
  pinMode(30, OUTPUT); // IN2
  pinMode(33, OUTPUT); // IN3
  pinMode(32, OUTPUT); // IN4

  // Relay
  digitalWrite(30,HIGH);
  digitalWrite(31,HIGH);
  digitalWrite(32,HIGH);
  digitalWrite(33,HIGH); 

  ls_x_beg.setDebounceTime(50); // set debounce time to 50 milliseconds
  ls_x_end.setDebounceTime(50); // set debounce time to 50 milliseconds
  ls_y_beg.setDebounceTime(50); // set debounce time to 50 milliseconds
  ls_y_end.setDebounceTime(50); // set debounce time to 50 milliseconds
  ls_z_beg.setDebounceTime(50); // set debounce time to 50 milliseconds
  ls_z_end.setDebounceTime(50); // set debounce time to 50 milliseconds

  stepper_x.setMaxSpeed(max_speed);
  stepper_y.setMaxSpeed(max_speed);
  stepper_z.setMaxSpeed(max_speed);

  stepper_x.setAcceleration(acceleration);
  stepper_y.setAcceleration(acceleration);
  stepper_z.setAcceleration(acceleration);

  // Then give them to MultiStepper to manage
  steppers.addStepper(stepper_x);
  steppers.addStepper(stepper_y);
  steppers.addStepper(stepper_z);
}

void loop() {
  // Read and process serial input
  processSerialInput();

  // Send current position
  sendCurrentPosition();

  // Loop relay
  digitalWrite(31,K1);
  digitalWrite(30,K2);
  digitalWrite(33,K3);
  digitalWrite(32,K4);

  ls_x_beg.loop();
  ls_x_end.loop();
  ls_y_beg.loop();
  ls_y_end.loop();
  ls_z_beg.loop();
  ls_z_end.loop();

  if (homing) {
    stepper_x.run();
    stepper_y.run();
    stepper_z.run();

    // Handle homing logic
    handleHoming();
  }


  // Handle limit switch logic
  handleLimitSwitches();
  // Multistepper move
  if (!homing) {
    steppers.run();
    multiStepperMove();
  }
}

void sendCurrentPosition() {
  // Send current position if movement occurred
  if (millis() - lastSendTime >= sendInterval) {
    if (stepper_x.currentPosition() != positions[0] || stepper_y.currentPosition() != positions[1] || stepper_z.currentPosition() != positions[2]) {
      stringCurrentPosition();
    }
    if (stepper_x.distanceToGo() == 0 || stepper_y.distanceToGo() == 0 || stepper_z.distanceToGo() == 0) {
      stringCurrentPosition();
    }
  lastSendTime = millis();
  }

}

void stringCurrentPosition() {
    // Concatenate and review extracted coordinates
  createSafeString (str_currentpos, 60);
  createSafeString (del, 3, ";");

  str_currentpos = "C";
  str_currentpos += stepper_x.currentPosition();
  str_currentpos += del;
  str_currentpos += stepper_y.currentPosition();
  str_currentpos += del;
  str_currentpos += stepper_z.currentPosition();

  Serial.println(str_currentpos);
}

void handleHoming() {
  if (home) {
    if (stepper_x.distanceToGo() == 0) {
      if (!x_beg) { // if 1st x-limit switch has not been pressed
        stepper_x.moveTo(stepper_x.currentPosition() - 100000); // move
      } else if (x_beg && !x_end) { // if 1st x-limit has been pressed but 2nd has not
        stepper_x.moveTo(stepper_x.currentPosition() + 100000); // move
      }
    }

    if (stepper_y.distanceToGo() == 0) {
      if (!y_beg) { // if 1st y-limit switch has not been pressed
        stepper_y.moveTo(stepper_y.currentPosition() - 100000); // move
      } else if (y_beg && !y_end) { // if 1st y-limit switch has been pressed but 2nd has not
        stepper_y.moveTo(stepper_y.currentPosition() + 100000); // move
      }
    }

    if (stepper_z.distanceToGo() == 0) {
      if (!z_beg) { // if 1st z-limit switch has not been pressed
        stepper_z.moveTo(stepper_z.currentPosition() - 100000); // move
      } else if (z_beg && !z_end) { // if 1st z-limit switch has been pressed but 2nd has not
        stepper_z.moveTo(stepper_z.currentPosition() + 100000); // move
      }
    }    
  }

  // Limit switch logic
  handleLimitSwitches();
}

void handleLimitSwitches() {
  if (x_beg || x_end || y_beg || y_end || z_beg || z_end) {
    Serial.println("Moving to: 0;0;0");
    // stepper_x.setCurrentPosition(positions[0]);
    // stepper_y.setCurrentPosition(positions[1]);
    // stepper_z.setCurrentPosition(positions[2]);
    createSafeString (str_limits, 60);
    createSafeString (del, 3, ";");

    str_limits = "L";
    str_limits += x_ceiling;
    str_limits += del;
    str_limits += y_ceiling;
    str_limits += del;
    str_limits += z_ceiling;
    Serial.println(str_limits);
    homing = false;
    home = false;
  }
  // x_range limit switch logic
  if(ls_x_beg.isPressed()) { // when 1st x-limit switch is pressed
    Serial.println("ls_x_beg pressed");
    if (home && !x_beg) { // if homing
      stepper_x.stop(); // stop motor
      x_beg = true; // stop moveTo
      x_end = true; // prevent reverse
      stepper_x.setSpeed(0); // stop instantly
      stepper_x.moveTo(stepper_x.currentPosition() + 500); // move past switch to release
    } else if (!home) {
      stepper_x.setCurrentPosition(positions[0]);
      stepper_x.stop();
      stepper_x.setSpeed(0);
      positions[0] = positions[0] + 500; // move past switch to release
    }
  }
  if(ls_x_beg.isReleased()) {
    Serial.println("ls_x_beg released");
    if (home && x_beg) {
      stepper_x.setCurrentPosition(0); // set reference point
      Serial.println("setting zero");
      Serial.println(stepper_x.currentPosition());
      stepper_x.setSpeed(max_speed); // instantly speed up
      x_end = false; // allow reverse
      Serial.println("homing x_end");
    }
  }

  if(ls_x_end.isPressed()) {
    Serial.println("ls_x_beg pressed");
    if (home && !x_end) {
      stepper_x.stop();
      x_end = true;
      stepper_x.setSpeed(0);
      stepper_x.moveTo(stepper_x.currentPosition() - 500); // move past switch to release
    } else if (!home) {
      stepper_x.setCurrentPosition(positions[0]);
      stepper_x.stop();
      stepper_x.setSpeed(0);
      positions[0] = positions[0] - 500; // move past switch to release
    }
  }
  if(ls_x_end.isReleased()) {
    Serial.println("ls_x_end released");
    if (home && x_end) {
      x_ceiling = stepper_x.currentPosition(); // set max position
      Serial.print("setting ceiling to: ");
      Serial.println(x_ceiling);
      Serial.println("homing y_beg");
      stepper_x.moveTo(0);
    }
  }

  // y_range limit switch logic
  if(ls_y_beg.isPressed()) { // when 1st y-limit switch is pressed
  Serial.println("ls_y_beg pressed");
    if (home && !y_beg) { // if homing
      stepper_y.stop(); // stop motor
      y_beg = true; // stop moveTo
      y_end = true; // prevent reverse
      stepper_y.setSpeed(0); // stop instantly
      stepper_y.moveTo(stepper_y.currentPosition() + 500); // move past switch to release
    } else if (!home) {
      stepper_y.setCurrentPosition(positions[1]);
      stepper_y.stop();
      stepper_y.setSpeed(0);
      positions[1] = positions[1] + 500; // move past switch to release
    }
  }
  if(ls_y_beg.isReleased()) {
    Serial.println("ls_y_beg released");
    if (home && y_beg) {
      stepper_y.setCurrentPosition(0); // set reference point
      Serial.println("setting zero");
      Serial.println(stepper_y.currentPosition());
      stepper_y.setSpeed(max_speed); // instantly speed up
      y_end = false; // allow reverse
      Serial.println("homing y_end");
    }
  }

  if(ls_y_end.isPressed()) {
    Serial.println("ls_y_end pressed");
    stepper_y.setCurrentPosition(positions[1]);
    stepper_y.stop();
    stepper_y.setSpeed(0);
    if (home && !y_end) {
      stepper_y.stop();
      y_end = true;
      stepper_y.setSpeed(0);
      stepper_y.moveTo(stepper_y.currentPosition() - 500); // move past switch to release
    } else if (!home) {
      stepper_y.setCurrentPosition(positions[1]);
      stepper_y.stop();
      stepper_y.setSpeed(0);
      positions[1] = positions[1] - 500; // move past switch to release
    }
  }
  if(ls_y_end.isReleased()) {
    Serial.println("ls_y_end released");
    if (home && y_end) {
      y_ceiling = stepper_y.currentPosition(); // set max position
      Serial.print("setting ceiling to: ");
      Serial.println(y_ceiling);
      stepper_y.moveTo(0);
    }
  }

  // z_range limit switch logic
  if(ls_z_beg.isPressed()) { // when 1st z-limit switch is pressed
    Serial.println("ls_z_beg pressed");
    if (home && !z_beg) { // if homing
      stepper_z.stop(); // stop motor
      z_beg = true; // stop moveTo
      z_end = true; // prevent reverse
      stepper_z.setSpeed(0); // stop instantly
      stepper_z.moveTo(stepper_z.currentPosition() + 500); // move past switch to release
    } else if (!home) {
      stepper_z.setCurrentPosition(positions[2]);
      stepper_z.stop();
      stepper_z.setSpeed(0);
      positions[2] = positions[2] + 500; // move past switch to release
    }
  }
  if(ls_z_beg.isReleased()) {
    Serial.println("ls_z_beg released");
    if (home && z_beg) {
      stepper_z.setCurrentPosition(0); // set reference point
      Serial.println("setting zero");
      Serial.println(stepper_z.currentPosition());
      stepper_z.setSpeed(max_speed); // instantly speed up
      z_end = false; // allow reverse
      Serial.println("homing z_end");
    }
  }

  if(ls_z_end.isPressed()) {
    Serial.println("ls_z_beg pressed");
    if (home && !z_end) {
      stepper_z.stop();
      z_end = true;
      stepper_z.setSpeed(0);
      stepper_z.moveTo(stepper_z.currentPosition() - 500); // move past switch to release
    } else if (!home) {
      stepper_z.setCurrentPosition(positions[2]);
      stepper_z.stop();
      stepper_z.setSpeed(0);
      positions[2] = positions[2] - 500; // move past switch to release
    }
  }
  if(ls_z_end.isReleased()) {
    Serial.println("ls_z_end released");
    if (home && z_end) {
      z_ceiling = stepper_z.currentPosition(); // set max position
      Serial.print("setting ceiling to: ");
      Serial.println(z_ceiling);
      stepper_z.moveTo(0);
    }
  }
}

void multiStepperMove() {
  // Move to the new positions if they are different
  if (stepper_x.currentPosition() != positions[0] || 
      stepper_y.currentPosition() != positions[1] || 
      stepper_z.currentPosition() != positions[2]) { 
    steppers.moveTo(positions);  // Use MultiStepper to move all steppers together
  }
}

void processSerialInput() {
  // read input
  if (Serial.available() > 0) {
    char input[100];
    createSafeString (strInput, sizeof(input));
    strInput = Serial.readStringUntil('\n').c_str();
    
    // Synchronize on connect
    if (strInput.indexOf("C") > -1) {
      strInput.remove(0,1); 
      // Create SafeStrings for the tokens
      createSafeString (str_x, 20);
      createSafeString (str_y, 20);
      createSafeString (str_z, 20);

      // Split the string and assign to variables
      strInput.stoken(str_x, 0, ";");
      size_t bufy = str_x.length()+1;
      strInput.stoken(str_y, bufy, ";");
      size_t bufz = bufy+str_y.length()+1;
      strInput.stoken(str_z, bufz, ";");

      // Assign positions
      positions[0] = atof(str_x.c_str());
      positions[1] = atof(str_y.c_str());
      positions[2] = atof(str_z.c_str());
      stepper_x.setCurrentPosition(positions[0]);
      stepper_y.setCurrentPosition(positions[1]);
      stepper_z.setCurrentPosition(positions[2]);
    }

    if (strInput == "H") {
      homing = true;
      home = false;
      x_beg = false;
      x_end = false;
      y_beg = false;
      y_end = false;
      z_beg = false;
      z_end = false;

      stepper_x.stop();
      stepper_y.stop();
      stepper_z.stop();
      stepper_x.setMaxSpeed(max_speed);
      stepper_y.setMaxSpeed(max_speed);
      stepper_z.setMaxSpeed(max_speed);

      Serial.println("homing x_beg");
      home = true;
    }

    if (strInput == "s") {
      home=false;
      homing=false;
      positions[0]=stepper_x.currentPosition();
      positions[1]=stepper_y.currentPosition();
      positions[2]=stepper_z.currentPosition();
    }

    if (strInput == "X") {
      K1 = !K1;
      K3 = K1;
      Serial.print("X: "); Serial.println(K1);
    }

    if (strInput == "Y") {
      K2 = !K2;
      K4 = K2;
      Serial.print("Y: "); Serial.println(K2);
    }

    // Regular mode movement
    if (strInput.indexOf("P") > -1) {
      strInput.remove(0,1); 
      // Create SafeStrings for the tokens
      createSafeString (str_x, 20);
      createSafeString (str_y, 20);
      createSafeString (str_z, 20);

      // Split the string and assign to variables
      strInput.stoken(str_x, 0, ";");
      size_t bufy = str_x.length()+1;
      strInput.stoken(str_y, bufy, ";");
      size_t bufz = bufy+str_y.length()+1;
      strInput.stoken(str_z, bufz, ";");

      // Assign positions
      positions[0] = atof(str_x.c_str());
      positions[1] = atof(str_y.c_str());
      positions[2] = atof(str_z.c_str());

      // Calculate the distance to the target for each stepper
      int distx = abs(stepper_x.currentPosition() - positions[0]);
      int disty = abs(stepper_y.currentPosition() - positions[1]);
      int distz = abs(stepper_z.currentPosition() - positions[2]);

      // Function to calculate speed based on distance
      auto calculateSpeed = [](int distance) {
        if (distance <= 10000) {
          return 0.0 + distance; // Set speed to 1 steps/s for distances <= 10
        } else {
          return 100000.0; // Cap the speed at 10000 steps/s for distances > 100
        }
      };

      // Set the maximum speed for each stepper based on the distance to the target
      stepper_x.setMaxSpeed(calculateSpeed(distx));
      stepper_y.setMaxSpeed(calculateSpeed(disty));
      stepper_z.setMaxSpeed(calculateSpeed(distz));
    }
  }
}