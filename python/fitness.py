import RPi.GPIO  as GPIO
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import datetime

#################################

# ADD TWILIO #

import os
from twilio.rest import TwilioRestClient
from credentials import account_sid, auth_token, my_cell, my_twilio
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
#client = Client(account_sid, auth_token)

#account_sid = os.environ['TWILIO_ACCOUNT_SID']
#auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# test twilio #
my_msg = "Twilio Test: This should be the first text that goes through"
message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)

# Functions #
def startSMS():
        my_msg = "Your workout is starting now"
        message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)

def bookSMS():
        my_msg = "Your gym has been booked: *** For Dev Purposes we can send the google maps link here"
        message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)

def halfSMS():
        global calories
        my_msg = ("You are half way through your workout. You have bruned ", calories)
        message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)

def endSMS():
        my_msg = "Your workout has ended: *** For Dev purposes we can send them a link to their data on the website. \n Schedule another session here: ***link"
        message = client.messages.create(to=my_cell, from_=my_twilio,body=my_msg)


###############################

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

#Twilio book sms
bookSMS()
#Twilio start sms
startSMS()

while True:
        if seconds>=30 and shake>=90 and seconds%30 ==  0:
                        calories =calories+1
                        print('You burned',str(calories))
        if calories >= a and seconds<=b*60:
                try:
                        sheet.row_values(i)
                        i=i+1
                except:
                        sheet.update_cell(i, 1, currentDT)
                        sheet.update_cell(i, 2, calories)
                        print('You have earned your goal and  burned',str(calories),'calories')
                        break
        elif seconds==b*60 and calories<a:
                print('Unfortunateley you have not reached your goal')
                break
        try:
                sheet2.row_values(z)
                z=z+1
        except:
                sheet2.update_cell(z, 1, currentDT)
                sheet2.update_cell(z, 2, shake)


        time.sleep(1)
        seconds = seconds+1
        print(seconds)
#Twilio end sms
endSMS()

