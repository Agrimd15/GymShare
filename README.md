# GymShare
## LA Hacks 2021
### SW-420 Motion Sensor
![download-7](https://user-images.githubusercontent.com/35862574/112741863-1354c900-8f3e-11eb-9e6a-cb56bc23d162.jpg)

The SW-420 sensor is a motion sensor with three pins (VCV, GND, CH_PIN)

To set up our hardware to work with our code you need to understand the pinout for the Raspberry Pi Zero W

![Raspberry-PI-Zero-Pinout-schema](https://user-images.githubusercontent.com/35862574/112744286-9896a880-8f53-11eb-98f8-9ddfec1b05ec.jpeg)

You need the VCV pin to go to the 5V pin on the pi
The GND port on the Ground port on the pi
The CH_pin has to go the pin of Channel 21 on the pi


From there all you need to do is run the program fitness.py on your raspberry pi, and you will have a working fitness tracker that can track the intensity of your training and the calories burned

As long as you have the pi and your laptop on the same wifi the pi should automatically connect to your dashboard and give you live updates on your workout

You can check out the intensity graph and the caloric loss graph on the website to see how your workout went

### Other components to the project

Twilio Api: We used this to give live updates and feedback to the user based on their inputs to the website and the data collected via the fitness tracker
Google Cloud: Maps Api to list gyms near you and locate gyms. Sign-in with google to make user profiles. 
Website: Functionality includes, data collection, dashboard with progress, and chat bot

 
 #### Credits
 LA Hacks 2021
 Gym Share
 Team: Sahil Tallam, Ishaan Bansal, Samarth Shah, Rohan Patra, Agrim Dhingra 
