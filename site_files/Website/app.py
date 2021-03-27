# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NcLAHn3af6eFwpYWWt_GtQNYzT_2Nkbh
"""


import pandas as pd
import numpy as np

import flask
from flask import Flask, render_template, request, redirect

from numpy import array
from numpy import argmax

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Import firebase stuff here
# import pyrebase
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("gymshare-1-firebase-adminsdk-my52k-0f3dc45d2d.json")
# firebase_admin.initialize_app(cred)

# config = {
#   "type": "service_account",
#   "project_id": "gymshare-1",
#   "private_key_id": "0f3dc45d2d7646fcc666988d7af0b9b6666fb10c",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDrLMGyMCphGEP5\nlJp4ltxWdCL19CsIsvc4LeWfBHjpj4HSMT5IMoqte7uWCWZHsnjMuSpVs991s9hI\nWKYG4/ksm0xR95jAywr9vKt+XIFdYj8WaEUuqEpw/UxgWA/SKNCLTHUcDKB/UXXY\nCP8tRTFdYA2xoxKNrBOhAGv45VAtLgB3AZNKG/igxx9HkSNuocV+GrCkYLlz4aNp\ntJGyGTY/sBJ5xAhl6APcwmAPGzOA+zjKh8v2t4nd4cYIdGmliK4vwdhXKtOBZ29q\ngSkL5CHhvGQXHNTku4cgxg+udHMG2OwhEibpYW7wiIm1jfa92GdHWsY2ViQpdriX\nbKsxpedvAgMBAAECggEAARHhGVWlNp5RO2QzcbH+XCf1u3uFvPVY6zMZKS5ZKeuR\nKXxPC3OsItS4UCalbpriYPrzNTdrTt3QK8AVTrm3luEKhp0dU7xKLo5Rqwm4DpMy\nhi7jtDmtrKbpnFpov6b04V4Sz5WgwdT4t9waQRM9dgXIhc0Iy1h4GXtEDh1Owr9N\nF/lDBfGj2Y/LybcKdSMcPvvqHjtikDiX515dPjC8E+kBDLWMTVnP4Y9nwXq20y9E\npdetp3Rgcxs2XDbNrK3s3gx5aUGD+W8Faci/OGcYbkzZKgF5fTQ7Bumafp6lA1iI\nW6gqarlyQaXE2vnZ4cVEIglqNHdLjcm2+qOeJieX4QKBgQD4DPrbvFfCc+6lJOox\nNk5hr7hsSzq6zOCj+egWljCBv1N8rGI+uOQyyrHF6ch0cHOHSGMuwooDBOiuMOyt\n2onNhAz76Yq+P1gG87FzZ7v7QRfIOCnf1AXNyyK8V2D5e7V1n/5yPha4wmesB8A9\nyUoNz0zwKRlO/Z2B9d8cmnblDwKBgQDytiR19lg8UypL8/Z1e3pJTTYxLPahq0ed\nEukch9jc2furFfj7Sstp8e5f2v8Jxwi3JpwquxRHPh4fZh+oQOYNnfKaOvLnIPdh\nNyvlNTIXJN9NWZ6T/+TyjBchWISMe0DBeZASM74GEqET/nVI3247d71h1/YNu6PJ\nKMm6f/yXoQKBgDNzrc1KggGpvoSu5Y0TsKp+ooiECkiZGreorMWSnbksEIs5zp8o\nBt2qQbnFxniwoqYbE8etPqdlq0YGi/F79T2V+IOAa/EOfpnijppbmBiD5gT38Wem\nORX43tmmXk0hpgAiEctsqZXlbU+3w96NFDlNGK5wN/m0jalZcNAkEiltAoGBAKcG\nSVkUSexZnwXdwYFfk+vVwrFcq+zdnc6uMNV9dvOk3tgBqvHjqtAhuVUls9Tar1i6\nrUWKsI3GZZxd/vMeljJQu57/aiE8QoEYIpD9ZpcevLzSK5rVwoxXc6Ny8uRp/Uon\nicm86cvsDgVgWv3nJEiwQhePMriIpFHOS+SYJw+BAoGBALS0WMRQied3GaQdLZLT\nvQXMSGToGw7DqSAsGNqehcZulZWSqXZm3R01SQ2x+OfSXhOoHuRfbwtcZShS20mY\n2N2dvrOLQ5m0JeVPhjTaE8Egd3LpPVaTV+jVLvNniowjTPeeb0GMEDR0BI1P2Luc\nhcmbKMHr/TupX5341pITzVWl\n-----END PRIVATE KEY-----\n",
#   "client_email": "firebase-adminsdk-my52k@gymshare-1.iam.gserviceaccount.com",
#   "client_id": "117680563318548326331",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-my52k%40gymshare-1.iam.gserviceaccount.com"
# }


# init firebase

# firebase = pyrebase.initialize_app(config)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gymshare-308916-8855f7671430.json', scope)
gc = gspread.authorize(credentials)

wks = gc.open('GymShare_FormData').sheet1



# End Firebase importing here

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



name_array = []
phone_array = []
height_array = []
weight_array = []

fitnessLevel_array = []

age_array = []

weightChoice_array = []

respiration_array = []
ventilator_array = []

muscles_array = []


@app.route('/send', methods=['GET', 'POST'])
def send():

    if request.method == "POST":

        req = request.form
        # print(req)

        name = req.get("name")
        name_array.append(name)
        name_array[0] = name

        phone = req.get("phone")
        phone_array.append(phone)
        phone_array[0] = phone

        height = req.get("height")
        height_array.append(height)
        height_array[0] = height
    

        weight = req.get("weight")
        weight_array.append(weight)
        weight_array[0] = weight


        fitnessLevel = req.get("fitnessLevel")
        fitnessLevel_array.append(fitnessLevel)
        fitnessLevel_array[0] = fitnessLevel

        age = req.get("age")
        age_array.append(age)
        age_array[0] = age

        weightChoice = req.get("weightChoice")
        weightChoice_array.append(weightChoice)
        weightChoice_array[0] = weightChoice

        respiration = req.get("respiration")
        respiration_array.append(respiration)
        respiration_array[0] = respiration

        muscles = req.get("muscles")
        muscles_array.append(muscles)
        muscles_array[0] = muscles

        message = req.get("message")
        
        print(muscles)


        # PROGRAM SECTION

        recommended_workouts = []

        # BMI = round(weight / (height*height), 2)

        # WEIGHT CHOICE

        if(weightChoice == "Reduce Weight"):
            recommended_workouts.append("Cardio")
            recommended_workouts.append("Balance")
            recommended_workouts.append("Flexibility")
            recommended_workouts.append("Muscular Endurance")
            recommended_workouts.append("Muscular Strength")
        elif(weightChoice == "Maintain Weight"):
            recommended_workouts.append("Cardio")
            recommended_workouts.append("Balance")
            recommended_workouts.append("Flexibility")
        elif(weightChoice == "Gain Weight"):
            recommended_workouts.append("Balance")
            recommended_workouts.append("Flexibility")
            recommended_workouts.append("Muscular Strength")

        # RESPIRATION

        if(respiration == "Yes"):
            recommended_workouts.append("Cardio")
            recommended_workouts.append("Balance")
            recommended_workouts.append("Flexibility")
            recommended_workouts.append("Muscular Endurance")
        
        # MUSCLES

        if(muscles == "Tone Muscles"):
            recommended_workouts.append("Cardio")
            recommended_workouts.append("Balance")
            recommended_workouts.append("Flexibility")
            recommended_workouts.append("Muscular Endurance")
        elif(muscles == "Build muscle mass"):
            recommended_workouts.append("Cardio")
            recommended_workouts.append("Balance")
            recommended_workouts.append("Flexibility")
            recommended_workouts.append("Muscular Strength")
            
        

        recommended_workouts = sorted(set(recommended_workouts))

        listToStr = ' '.join([str(elem) for elem in recommended_workouts]) 


        print(recommended_workouts)


        wks.append_row([name, phone, height, weight, fitnessLevel, age, weightChoice, respiration, muscles, message, listToStr])


        return redirect(request.url)

    return render_template('index.html')



if __name__ == "__main__":
    app.debug = True
    app.run()