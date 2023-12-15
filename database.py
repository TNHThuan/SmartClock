import pyrebase
import serial

config = {     
  "apiKey": "AIzaSyAZY4-tUxYDhQVnAPUeDgXVp8P89YVSepo",
  "authDomain": "kltn-ffac4.firebaseapp.com",
  "databaseURL": "https://kltn-ffac4-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "kltn-ffac4.appspot.com"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database().child("users").child("2019")