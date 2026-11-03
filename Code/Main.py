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


  # This turns ALL alarms in the list ON (True) or OFF (False)
    def toggle_all(self, turn_on):
        # Go through every alarm one by one
        for alarm in self.alarms:
            # Set this alarm to ON or OFF
            alarm.is_active = turn_on

    # This puts the alarms in order from the earliest time to the latest
    def sort_alarms(self):
        # Sort the list, using each alarm's time as the thing to compare
        self.alarms.sort(key=lambda alarm: alarm.time)

    # This checks if the list already has an alarm at a given time
    def has_time(self, time):
        # Go through every alarm one by one
        for alarm in self.alarms:
            # If this alarm has the same time
            if alarm.time == time:
                # Answer yes
                return True
        # We checked every alarm and found no match, so answer no
        return False

    # This turns off every alarm that is still to come after the time "now"
    def i_woke_up(self, now):
        # Start counting how many alarms we turn off
        count = 0
        # Go through every alarm one by one
        for alarm in self.alarms:
            # Check if the alarm is later than now AND still ON
            if alarm.time > now and alarm.is_active:
                # Turn this alarm OFF
                alarm.is_active = False
                # Add 1 to our counter
                count += 1
        # Give back how many alarms were turned off
        return count

    # This gives the days of the list as short text, like "Mon-Fri" or "Mon, Wed, Fri"
    def days_text(self):
        # If the list rings on all 7 days
        if len(self.days) == 7:
            # Give back "Every day"
            return "Every day"
        # If the list rings Monday to Friday
        if self.days == [0, 1, 2, 3, 4]:
            # Give back "Mon-Fri"
            return "Mon-Fri"
        # If the list rings only on the weekend
        if self.days == [5, 6]:
            # Give back "Sat, Sun"
            return "Sat, Sun"
        # Start with an empty list of day names
        names = []
        # Go through every chosen day number
        for day in self.days:
            # Turn the number into a name like "Mon" and add it
            names.append(DAY_NAMES[day].capitalize())
        # Join the names with commas, like "Mon, Wed, Fri"
        return ", ".join(names)

    # This gives one line of text that describes the list (used on the home screen)
    def summary(self):
        # Start counting how many alarms are ON
        active_count = 0
        # Go through every alarm one by one
        for alarm in self.alarms:
            # If this alarm is ON
            if alarm.is_active:
                # Add 1 to our counter
                active_count += 1
        # Get the time of the first alarm as text
        first = self.alarms[0].time.strftime(TIME_FORMAT)
        # Get the time of the last alarm as text
        last = self.alarms[-1].time.strftime(TIME_FORMAT)
        # Give back the line; the <12 pads the name to 12 characters so columns line up
        return f"{self.name:<12}{first} - {last}   {self.days_text()}   {active_count} of {len(self.alarms)} ON"

    # This prints the list name and all its alarms
    def show(self):
        # Print the list name, how many alarms it has, and the days it rings on
        print(f"\n{self.name} ({len(self.alarms)} alarms) - {self.days_text()}")
        # Go through every alarm one by one
        for alarm in self.alarms:
            # Print this alarm
            print(alarm)


# This class saves the alarm lists to a CSV file and loads them back
class FileManager:
    # This runs when we make a new FileManager
    def __init__(self, filename):
        # Save the name of the file we will use
        self.filename = filename

    # This writes all the alarm lists into the CSV file
    def save_to_file(self, alarm_lists):
        # Open the file for writing ("w"); it is closed automatically after the block
        with open(self.filename, "w", newline="") as file:
            # Make a writer that knows how to write CSV rows
            writer = csv.writer(file)
            # Write the first row with the column names
            writer.writerow(["list_name", "time", "is_active", "days"])
            # Go through every alarm list
            for alarm_list in alarm_lists:
                # Go through every alarm inside this list
                for alarm in alarm_list.alarms:
                    # Turn the day numbers into text like "0 1 2 3 4"
                    days_text = " ".join(str(day) for day in alarm_list.days)
                    # Write one row: list name, time as text, ON/OFF state, and the days
                    writer.writerow([alarm_list.name, alarm.time.strftime(TIME_FORMAT), alarm.is_active, days_text])

    # This reads the CSV file and rebuilds the alarm lists
    def load_from_file(self):
        # This dictionary connects a list name to its AlarmList object
        lists_by_name = {}
        # Try to open the file (it might not exist yet)
        try:
            # Open the file for reading ("r")
            with open(self.filename, "r", newline="") as file:
                # Make a reader that gives each row as a dictionary
                reader = csv.DictReader(file)
                # Go through every row in the file
                for row in reader:
                    # Get the list name from this row
                    name = row["list_name"]
                    # If we have not seen this list name yet
                    if name not in lists_by_name:
                        # Make a new empty AlarmList with that name
                        lists_by_name[name] = AlarmList(name)
                        # Read the days text from this row (older files may not have it)
                        days_text = row.get("days")
                        # If the row has days saved
                        if days_text:
                            # Start with no days
                            lists_by_name[name].days = []
                            # Go through each day number in the text
                            for day_text in days_text.split():
                                # Turn the text into a number and add it
                                lists_by_name[name].days.append(int(day_text))
                    # Turn the time text (like "07:05") back into a time object
                    time = datetime.strptime(row["time"], TIME_FORMAT).time()
                    # Turn the text "True" or "False" back into a real True or False
                    is_active = (row["is_active"] == "True")
                    # Make the alarm and add it to the right list
                    lists_by_name[name].alarms.append(Alarm(time, name, is_active))
        # If the file does not exist (first time running the program)
        except FileNotFoundError:
            # Do nothing; we just start with no lists
            pass
        # Give back all the lists we loaded
        return list(lists_by_name.values())


# This class is the app: it shows the screens and connects everything together
class AlarmApp:
    # This runs when the app starts
    def __init__(self):
        # Make a FileManager that uses our CSV file
        self.file_manager = FileManager(FILE_NAME)












