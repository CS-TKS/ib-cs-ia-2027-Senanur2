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
        # Load saved lists from the file (empty if nothing was saved)
        self.alarm_lists = self.file_manager.load_from_file()
        # This is True while the alarms are running (the clock is being watched)
        self.running = False
        # This holds the alarm that is ringing right now (None means nothing is ringing)
        self.ringing_alarm = None
        # This holds the list that the ringing alarm belongs to
        self.ringing_list = None

        # This clears the terminal so each screen looks clean

    def clear_screen(self):
        # If this computer is Windows
        if sys.platform.startswith("win"):
            # Windows uses the command "cls" to clear the screen
            os.system("cls")
        # If this is a Mac or Linux computer with a real terminal (TERM is set)
        elif "TERM" in os.environ:
            # Mac and Linux use the command "clear"
            os.system("clear")
        # If there is no real terminal (like PyCharm's Run window)
        else:
            # Print 40 empty lines to push the old text out of view instead
            print("\n" * 40)

        # This clears the screen and prints a title at the top

    def show_title(self, title):
        # Clear the screen first
        self.clear_screen()
        # Print a line of 50 "=" signs
        print("=" * 50)
        # Print the title in the middle of 50 characters
        print(title.center(50))
        # Print another line of 50 "=" signs
        print("=" * 50)
        # If an alarm is ringing right now
        if self.ringing_alarm is not None:
            # Show a reminder on every screen so the user knows how to answer it
            print("*** ALARM RINGING! Type W (I woke up) or S (snooze) + Enter ***")

        # This waits for the user to press Enter so they can read the screen

    def pause(self):
        # Show the message and wait for Enter
        self.ask("\nPress Enter to go back to the menu...")

        # This shows the home screen: today's date and all the saved lists

    def show_dashboard(self):
        # Show the app title
        self.show_title("ALARM MANAGER")
        # Print today's day, date and time
        print(datetime.now().strftime("%A, %d %B %Y   %H:%M"))
        # Tell the user the alarms are working by themselves
        print("Alarms are ON. Keep this window open so they can ring.")
        # Show when the next alarm will ring
        print(f"Next alarm: {self.next_alarm_text()}")
        # Print the heading for the lists
        print("\nYOUR ALARM LISTS")
        # If there are no lists yet
        if not self.alarm_lists:
            # Tell the user how to make one
            print("  (none yet - create one with option 1)")
        # Go through the lists and number them starting at 1
        for number, alarm_list in enumerate(self.alarm_lists, start=1):
            # Print the number and the one-line summary of the list
            print(f"  {number}. {alarm_list.summary()}")

        # This asks for a time and keeps asking until the user types a valid one

    def ask_time(self, prompt):
        # Repeat forever until we return a good answer
        while True:
            # Ask the user and remove extra spaces from their answer
            text = self.ask(prompt).strip()
            # Try to turn the text into a time
            try:
                # If it works, give the time back and stop repeating
                return datetime.strptime(text, TIME_FORMAT)
            # If the text was not a valid time
            except ValueError:
                # Tell the user what went wrong, then the loop asks again
                print("Invalid time. Use 24-hour HH:MM, for example 07:30.")

        # This asks for the minutes between alarms and keeps asking until it is valid

    def ask_interval(self):
        # Repeat forever until we return a good answer
        while True:
            # Try to turn the answer into a whole number
            try:
                # Ask the user and convert their answer to an integer
                minutes = int(self.ask("Minutes between alarms (e.g. 5): "))
                # Check the number is bigger than 0
                if minutes > 0:
                    # If so, give it back and stop repeating
                    return minutes
                # Otherwise tell the user the number was too small
                print("The interval must be more than 0.")
            # If the answer was not a whole number
            except ValueError:
                # Tell the user what went wrong, then the loop asks again
                print("Please enter a whole number.")

        # This asks which days a list should ring on and keeps asking until it understands

    def ask_days(self):
        # Explain how to answer
        print("\nWhich days should this list ring?")
        # Show examples
        print("Type days like: mon wed fri   or: weekdays, weekend, everyday")
        # Repeat until we get a good answer
        while True:
            # Ask the user, remove extra spaces, and make it lowercase
            text = self.ask("Days (press Enter for every day): ").strip().lower()
            # If the user just pressed Enter
            if text == "":
                # Use every day
                return [0, 1, 2, 3, 4, 5, 6]
            # Start with no days chosen
            days = []
            # Remember if we understood every word
            understood = True
            # Go through each word (commas count as spaces)
            for word in text.replace(",", " ").split():
                # If the word means every day
                if word in ("everyday", "all"):
                    # Add Monday to Sunday
                    days.extend(range(7))
                # If the word means Monday to Friday
                elif word == "weekdays":
                    # Add Monday to Friday
                    days.extend(range(5))
                # If the word means the weekend
                elif word == "weekend":
                    # Add Saturday and Sunday
                    days.extend([5, 6])
                # If the first 3 letters are a day name (so "monday" works too)
                elif word[:3] in DAY_NAMES:
                    # Add that day's number
                    days.append(DAY_NAMES.index(word[:3]))
                # If we do not know the word
                else:
                    # Remember that something was not understood
                    understood = False
            # If every word was understood and at least one day was chosen
            if understood and len(days) > 0:
                # Give back the days: set() removes repeats, sorted() puts them in order
                return sorted(set(days))
            # Otherwise tell the user and ask again
            print("Sorry, I did not understand that. Example: mon wed fri")

        # This shows all lists and lets the user pick one

    def choose_list(self):
        # If there are no lists at all
        if not self.alarm_lists:
            # Tell the user to make one first
            print("\nNo lists yet. Create one first (option 1).")
            # Give back None, which means "nothing was chosen"
            return None
        # Print an empty line for spacing
        print()
        # Go through the lists and number them starting at 1
        for number, alarm_list in enumerate(self.alarm_lists, start=1):
            # Print the number and the list name
            print(f"{number}. {alarm_list.name}")
        # Repeat until the user picks a valid number
        while True:
            # Try to turn the answer into a whole number
            try:
                # Ask the user and convert their answer to an integer
                choice = int(self.ask("Choose a list number: "))
                # Check the number is between 1 and the number of lists
                if 1 <= choice <= len(self.alarm_lists):
                    # Give back the chosen list (Python counts from 0, so subtract 1)
                    return self.alarm_lists[choice - 1]
                # Otherwise tell the user the number does not exist
                print("That number is not in the list.")
            # If the answer was not a whole number
            except ValueError:
                # Tell the user what went wrong, then the loop asks again
                print("Please enter a number.")

        # This is menu option 1: make a new alarm list

    def create_list(self):
        # Show the screen title
        self.show_title("CREATE AN ALARM LIST")
        # Ask for the list name and remove extra spaces
        name = self.ask("Name of the new list (e.g. School): ").strip()
        # Check if the user typed nothing
        if name == "":
            # Tell the user the name is needed
            print("The name cannot be empty.")
            # Leave this function early
            return
        # Go through the lists we already have
        for existing in self.alarm_lists:
            # Compare names ignoring capital letters ("School" equals "school")
            if existing.name.lower() == name.lower():
                # Tell the user the name is taken
                print("A list with that name already exists.")
                # Leave this function early
                return

        # Ask for the start time (this keeps asking until it is valid)
        start = self.ask_time("Start time (HH:MM): ")
        # Repeat until the end time is acceptable
        while True:
            # Ask for the end time (this keeps asking until it is valid)
            end = self.ask_time("End time (HH:MM, same as start for one alarm): ")
            # Check the end time is not before the start time
            if end >= start:
                # It is fine, so stop repeating
                break
            # Otherwise tell the user what is wrong, then ask again
            print("The end time must be the same as or after the start time.")
        # Ask for the minutes between alarms
        interval = self.ask_interval()
        # Ask which days the list should ring on
        days = self.ask_days()

        # Make a new empty alarm list with the chosen name
        new_list = AlarmList(name)
        # Fill the list with alarms using the start, end and interval
        new_list.generate_alarms(start, end, interval)
        # Save the chosen days in the list
        new_list.days = days
        # Add the new list to our big list of lists
        self.alarm_lists.append(new_list)
        # Save everything to the file so it is not lost
        self.file_manager.save_to_file(self.alarm_lists)
        # Tell the user it worked and how many alarms were made
        print(f"\nCreated '{name}' with {len(new_list.alarms)} alarms ({new_list.days_text()}).")

        # This is menu option 2: show the alarms in a list

    def view_alarms(self):
        # Show the screen title
        self.show_title("VIEW ALARMS")
        # Let the user pick a list
        chosen = self.choose_list()
        # If a list was really chosen (not None)
        if chosen:
            # Print its alarms
            chosen.show()

        # This is menu option 4: turn a whole list ON or OFF

    def toggle_list(self):
        #Show the screen title
        #Let the user pick a list
        #If nothing was chosen
    #I need to add an 'if' function here..
        # Leave this function early
        # Ask ON or OFF, remove spaces, and make it lowercase
        # If the user typed "on"
# then i can add an elif here incase user types 'off'
        # If the user typed "off"
        # Turn every alarm in the list OFF
        # If the user typed anything else
# Save the change to the file
# Tell the user it worked
# This is menu option 5: delete a whole list
# Show the screen title
# If nothing was chosen
# Leave this function early
# Ask the user to confirm, because deleting cannot be undone
# If the user typed "y"
# Remove the list from our lists
# Save the change to the file
# If the user typed anything else
# This lets the user pick one alarm from a list by its number
# Repeat until the user picks a valid number
# Try to turn the answer into a whole number
# Ask the user and convert their answer to an integer
# Check the number is between 1 and the number of alarms
# Give back the chosen alarm (Python counts from 0, so subtract 1)
# otherwise tell the user the number does not exist
# Tell the user what went wrong, then the loop asks again
















