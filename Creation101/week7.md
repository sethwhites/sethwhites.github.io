# Week 7: Embedded Programming

This week I made an arduino blink in tinkerCAD. It was eerily similar to what I did in week 3. :)

## Light Off:

![arduinoblink_off](arduinoblink_off.PNG)

## Light On:

![arduinoblink_on](arduinoblink_on.PNG)

## Parts Used:

![arduinoblink_parts](arduinoblink_parts.PNG)

## Code:

``` C
/*
  This program blinks pin 13 of the Arduino (the
  built-in LED)
*/

void setup()
{
  pinMode(13, OUTPUT);
}

void loop()
{
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(13, HIGH);
  delay(1000); // Wait for 1000 millisecond(s)
  // turn the LED off by making the voltage LOW
  digitalWrite(13, LOW);
  delay(1000); // Wait for 1000 millisecond(s)
}
```
