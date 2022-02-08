#include <Ultrasonic.h>

// System time parameters in seconds
int trafficGreenTime = 10;
int trafficYellowTime = 3;
int trafficRedTime =3;
int redFlashingTime = 3; 
int delayAfterPedestrianButton = 1;
int fallBackTime = 120;

// Define buzz pin
const int buzzer = 10; 

// Define pedestrian LED pins
const int pedestrianGreen = 8;
const int pedestrianRed = 9;

// Define traffic LED pins
const int trafficGreen = 5;
const int trafficYellow = 6;
const int trafficRed = 7;

// Define pins for ultrasonic and buzzer
const int trigPin = 12;
const int echoPin = 13;
Ultrasonic ultrasonic(trigPin, echoPin);

// Define push button pin
const int pushButtonPin = 2;

// Define parameters for miliseconds to seconds
const int seconds = 1000;

// Debounce wait stable in milliseconds
const int debounceDelay = 50;

// Define sonar distance
int distance;

// Define sonar threshold distance in centimeters
int thresholdDistance = 30;  

// Pedestrian red light flashing frequency in seconds
float flashingTimePeriod = 0.2;

// Traffic red light start timestamp
unsigned long trafficRedStartTime;

void setup() {
  // Initialize pedestrian LED digital pins as an output.
  pinMode(pedestrianGreen, OUTPUT);
  pinMode(pedestrianRed, OUTPUT);

  // Initialize traffic LED digital pins as an output.
  pinMode(trafficGreen, OUTPUT);
  pinMode(trafficYellow, OUTPUT);
  pinMode(trafficRed, OUTPUT);

  // Initialize buzz digital pins as an output.
  pinMode(pedestrianGreen, OUTPUT);
  pinMode(pedestrianRed, OUTPUT);

  // Initialize buzzer digital pins as an output.
  pinMode(buzzer, OUTPUT);

  // Initialize push button digital pin as an input.
  pinMode(pushButtonPin, INPUT);

  // Serial print
  Serial.begin(9600);

  // Initial state
  // T: Red & P: Green
  digitalWrite(trafficRed, HIGH);
  digitalWrite(trafficYellow, LOW);
  digitalWrite(trafficGreen, LOW);
  digitalWrite(pedestrianGreen, HIGH);
  digitalWrite(pedestrianRed, LOW);
  digitalWrite(buzzer, LOW);
  trafficRedStartTime = millis();
}

void loop() {
   // Read distance from sonar
  distance = ultrasonic.read();

  // T: Red & P: Green
  digitalWrite(trafficRed, HIGH);
  digitalWrite(trafficYellow, LOW);
  digitalWrite(trafficGreen, LOW);
  digitalWrite(pedestrianGreen, HIGH);
  digitalWrite(pedestrianRed, LOW);
  digitalWrite(buzzer, LOW);
  
  // If vehicle detected or fall-back time arrived
  if ( (distance <= thresholdDistance && distance >= 0 ) || (millis() - trafficRedStartTime > 120*seconds) ) {

    digitalWrite(buzzer, HIGH);
    delay(1*seconds); 
    digitalWrite(buzzer, LOW);
    unsigned long redFlashingStartTime = millis();

    // T:Red & P: RedFlash
    // Red light flashing with 5Hz
    while (millis() - redFlashingStartTime <= redFlashingTime*seconds){
      digitalWrite(trafficRed, HIGH);
      digitalWrite(trafficYellow, LOW);
      digitalWrite(trafficGreen, LOW);
      digitalWrite(pedestrianGreen, LOW);
      digitalWrite(pedestrianRed, HIGH);
      digitalWrite(buzzer, HIGH);
      delay(flashingTimePeriod*seconds);
      digitalWrite(trafficRed, HIGH);
      digitalWrite(trafficYellow, LOW);
      digitalWrite(trafficGreen, LOW);
      digitalWrite(pedestrianGreen, LOW);
      digitalWrite(pedestrianRed, LOW);
      digitalWrite(buzzer, LOW);
      delay(flashingTimePeriod*seconds);
    }

    // T: Red & P: Red
    digitalWrite(trafficRed, HIGH);
    digitalWrite(trafficYellow, LOW);
    digitalWrite(trafficGreen, LOW);
    digitalWrite(pedestrianGreen, LOW);
    digitalWrite(pedestrianRed, HIGH);
    digitalWrite(buzzer, LOW);
    delay(trafficRedTime*seconds);
    
    // T: Green & P: Red
    digitalWrite(trafficRed, LOW);
    digitalWrite(trafficYellow, LOW);
    digitalWrite(trafficGreen, HIGH);
    digitalWrite(pedestrianGreen, LOW);
    digitalWrite(pedestrianRed, HIGH);
    digitalWrite(buzzer, LOW);
    
    // Listening push button input for 10 seconds
    unsigned long trafficGreenStartTime = millis();
    while(millis()-trafficGreenStartTime <= trafficGreenTime*seconds){
      if(debounce(pushButtonPin) == HIGH){
        Serial.print("PRESSED\n");
        delay(delayAfterPedestrianButton*seconds);
        break;
      }
    }

    // T: Yellow & P: Red
    digitalWrite(trafficRed, LOW);
    digitalWrite(trafficYellow, HIGH);
    digitalWrite(trafficGreen, LOW);
    digitalWrite(pedestrianGreen, LOW);
    digitalWrite(pedestrianRed, HIGH);
    digitalWrite(buzzer, LOW);
    delay(trafficYellowTime*seconds);

    // T: Red & P: Red
    digitalWrite(trafficRed, HIGH);
    digitalWrite(trafficYellow, LOW);
    digitalWrite(trafficGreen, LOW);
    digitalWrite(pedestrianGreen, LOW);
    digitalWrite(pedestrianRed, HIGH);
    digitalWrite(buzzer, LOW);
    delay(trafficRedTime*seconds);
    trafficRedStartTime = millis();
  }
  delay(10);                              
}

// debounce returns the stable switch state 
boolean debounce(int pin)
{
  boolean state;
  boolean previousState; 

  // store switch state 
  previousState = digitalRead(pin);          
  for(int counter=0; counter < debounceDelay; counter++)
  {
      // wait for 1 millisecond
      delay(1);      
      // read the pin             
      state = digitalRead(pin);
      if( state != previousState)
      {
         // reset the counter if the state changes
         counter = 0;
         // and save the current state 
         previousState = state;
      }
  }     
  return state;   
}
