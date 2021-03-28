import os
import RPi.GPIO  as GPIO
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import datetime

#Twilio
from twilio.rest import TwilioRestClient
from credentials import account_sid, auth_token, my_cell, my_twilio
from twilio.rest import Client
#account_sid = os.environ['TWILIO_ACCOUNT_SID']
#auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

#testmessage
my_msg = "Hey"
message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)

#code
currentDT = str(datetime.datetime.now())
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('fitness-pro-308916-607b89e77902.json', scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("Fitness Caloric User Data").sheet1
sheet2 = client.open("Fitness Intensity User Data").sheet1
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
i = 1
z = 1
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
print(requests.get('http://rohanpatra.a2hosted.com/GymShare/test.php?method=rasp_ip').text)

seconds = 0
calories = 0
shake = 0

print('How many calories would you like to burn?')
a=int(input())
print('How long would you like to work out?(in minutes)')
b=int(input())
def callback(channel):
        global shake
        global calories
        global seconds
        if GPIO.input(channel):

                shake=shake+1
                print('Shake:',str(shake))
        else:
                print('Movement Detected')
                shake=shake+1
                print('Shake:',str(shake))
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(channel, callback)

while True:
        try:
                sheet2.row_values(z)
                z=z+1
        except:
                sheet2.update_cell(z, 1, currentDT)
                sheet2.update_cell(z, 2, shake)
        if seconds>=30 and shake>=90 and seconds%30 ==  0:
                calories =calories+1
        if calories >=  a and seconds<=b*60:
                try:
                        sheet.row_values(i)
                        i=i+1
                except:
                        sheet.update_cell(i, 1, currentDT)
                        sheet.update_cell(i, 2, calories)
                        print('You have earned your goal and  burned',str(calories),'calories')
                        my_msg = ('You have earned your goal and  burned',str(calories),'calories')
                        message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)
                        break
        elif seconds==b*60 and calories<a:
                print('Unfortunateley you have not reached your goal')
                my_msg = "Unfortunateley you have not reached your goal"
                message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)
                break
        #sms
        if seconds == 1:
            my_msg = "Your workout will be starting soon"
            message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)
        if calories == (a/2):
            my_msg = "You are half way to your goal of ",a," calories, keep it up!"
            message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)
            
        time.sleep(1)
        seconds = seconds+1
        print(seconds)


        
