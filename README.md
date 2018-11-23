# Intelligent Medicine Box
Software Engineering Course Project (BITS Pilani K. K. Birla Goa Campus) IS F341

This is the server backend code that gathers weight changes from weight sensors on a Raspberry Pi-enabled medicine box, and uses it to sends anomaly notifications to the patient and doctor as per needed through the companion android app. 

It also keeps track of the medicines in the box along side the prescription timings.

## Dependencies:

Python 3, Pyrebase library, A Firebase account and authentication key

## Instructions for Deployment:

1. Installing firebase-admin library: <br>
$ sudo pip install pyrebase
1. To run tests: (Will take about 8 minutes to run) <br>
$ pytest src/test*.py
1. To start the server: <br>
$ python3 src/main.py

## Usage Instructions:

While running main, it will prompt for patient's email and password to login. After logging in, a new window will allow patient to give medicine box number (0 to 5 as per the current prescription), and give the new weight of medicines in that box.

It will calculate the difference in weight, count the number of pills, and compare it with the number of pills in prescripton, send an alert to firebase/Android App if needed. The alert will be shown on Android App.

## Team : 
Hackstreet boys:
1. Ravishankar Joshi
2. Anish Bhobe
3. Sugam Budhraja
4. Ameya Sinha
5. Abhiraj Hinge
