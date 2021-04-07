# Week 11: Networking and Communications

This week I set up tile to use with my phone and also keys using a tile sticker.

Tile was very intuitive and the setup was minimal.

<img src="tile_findthing_img.jpg" alt="tile_findthing_img" width="300"/>

For testing I took my keys and put them into another room and was able to find them using the tile app.

<img src="tile_fob_img.jpg" alt="tile_fob_img" width="400"/>


``` c++
const int outputPin = 8;
const int buttonPin = 9;

long int timer = 0;
bool run_driver = 0;
bool button_Flag = 0;
void setup() {
  pinMode(outputPin, OUTPUT); // sets the digital pin 8 as output, default is HIGH b/c of a pull-up resistor
  pinMode(buttonPin, INPUT);  // sets the digital pin 7 as an input, default is LOW b/c of a pull-down resistor  
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if(buttonState == 1)
  {
    button_flag != button_flag;
    delay(50);
  }
  if(timer >= 1000 || button_flag == 0)
    {} //do nothing
  else
  {
    if(run_driver == HIGH)
      digitalWrite(outputPin,HIGH);
    else
      digitalWrite(outputPin,LOW);
    run_driver != run_driver;
    timer ++;
    delay(60); // delays 60 ms every loop
  }
}
```
