# the csv tool so that i can save and read the CSv
import csv

#clear the screen and play a sounf on Mac
import os

#find out which type of computer is running the program
import sys

#clock can be watched at the same time as the user types
import threading

# Import datetime (to read and make times) and timedelta (to add minutes to a time)
from datetime import datetime, timedelta

# Import sleep so the program can wait for a number of seconds
from time import sleep

# This is how times are written: 24-hour, like 07:05
TIME_FORMAT = "%H:%M"

# This is the name of the file where everything is saved
FILE_NAME = "alarms.csv"

# These are the short day names; a day's position is its number (Monday is 0, like Python's weekday())
DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

class Alarm:
    #this runs when we make anew Alarm and sets up its information
    def __init__(self, time,label, is_active = True):
        self.time= time
        self.label=label
        self.is_active = is_active
    #this decides how an alrm looks when we print it
    def __str__(self):
        status = "ON" if self.is_active else "OFF"
        return f"{self.time.strftime(TIME_FORMAT) [{status}] {self.label}}"



class AlarmList:
    #this will run when we make a new alarm list
    def __init__ (self,name):
        self.name=name
        self.alarms = []
        self.days = [0,1,2,3,4,5,6]

    def generate_alarms (self, start, end, interval_minutes):
        current = start

        while current <= end:
            self.alarms.apend(Alarm(current.time(), self.name))
            current = current + timedelta(minutes = interval_minutes)

   def add_alarm(self, time):
       for alarm in self.alarms:

           if alarm.time == time:
               return False

           new_alarm = Alarm(time,self.name)

           position = 0

           while position < len(self.alarms) and self.alarms[position].time <time:
               position += 1

           self.alarms.insert(position, new_alarm)
           reutrn True


   def toggle_all(self, turn_on):













