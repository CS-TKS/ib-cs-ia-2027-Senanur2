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
        return f"{self.time.strftime(TIME_FORMAT)}  [{status}]  {self.label}"



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
           return True


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
        # Show the screen title
        self.show_title("TURN A LIST ON OR OFF")
        # Let the user pick a list
        chosen = self.choose_list()
        # If nothing was chosen
        if chosen is None:
            # Leave this function early
            return
        # Ask ON or OFF, remove spaces, and make it lowercase
        answer = self.ask("Turn the list ON or OFF? (on/off): ").strip().lower()
        # If the user typed "on"
        if answer == "on":
            # Turn every alarm in the list ON
            chosen.toggle_all(True)
        # If the user typed "off"
        elif answer == "off":
            # Turn every alarm in the list OFF
            chosen.toggle_all(False)
        # If the user typed anything else
        else:
            # Tell the user what to type
            print("Please type 'on' or 'off'.")
            # Leave this function early
            return
        # Save the change to the file
        self.file_manager.save_to_file(self.alarm_lists)
        # Tell the user it worked
        print(f"\nAll alarms in '{chosen.name}' are now {answer.upper()}.")

        # This is menu option 5: delete a whole list
def delete_list(self):
            # Show the screen title
            self.show_title("DELETE A LIST")
            # Let the user pick a list
            chosen = self.choose_list()
            # If nothing was chosen
            if chosen is None:
                # Leave this function early
                return
            # Ask the user to confirm, because deleting cannot be undone
            answer = self.ask(f"Delete '{chosen.name}' for good? (y/n): ").strip().lower()
            # If the user typed "y"
            if answer == "y":
                # Remove the list from our lists
                self.alarm_lists.remove(chosen)
                # Save the change to the file
                self.file_manager.save_to_file(self.alarm_lists)
                # Tell the user it worked
                print(f"\n'{chosen.name}' was deleted.")
            # If the user typed anything else
            else:
                # Tell the user nothing was deleted
                print("\nNothing was deleted.")

        # This lets the user pick one alarm from a list by its number
def choose_alarm(self, alarm_list):
            # Repeat until the user picks a valid number
            while True:
                # Try to turn the answer into a whole number
                try:
                    # Ask the user and convert their answer to an integer
                    choice = int(self.ask("Alarm number: "))
                    # Check the number is between 1 and the number of alarms
                    if 1 <= choice <= len(alarm_list.alarms):
                        # Give back the chosen alarm (Python counts from 0, so subtract 1)
                        return alarm_list.alarms[choice - 1]
                    # Otherwise tell the user the number does not exist
                    print("That number is not in the list.")
                # If the answer was not a whole number
                except ValueError:
                    # Tell the user what went wrong, then the loop asks again
                    print("Please enter a number.")

        # This is menu option 3: add, change or remove the alarms in a list
def edit_list(self):
            # Show the screen title
            self.show_title("EDIT A LIST")
            # Let the user pick a list
            chosen = self.choose_list()
            # If nothing was chosen
            if chosen is None:
                # Wait for Enter so the user can read the message
                self.pause()
                # Leave this function early
                return
            # This holds a short message to show at the top of the next screen
            message = ""
            # Repeat until the user chooses to go back
            while True:
                # Show the title with the name of the list
                self.show_title(f"EDIT: {chosen.name}")
                # If there is a message from the last action
                if message != "":
                    # Show the message
                    print(f"\n>> {message}")
                    # Clear the message so it only shows once
                    message = ""
                # Show which days this list rings on
                print(f"\nRings on: {chosen.days_text()}")
                # Print an empty line for spacing
                print()
                # Go through the alarms and number them starting at 1
                for number, alarm in enumerate(chosen.alarms, start=1):
                    # Print the number and the alarm
                    print(f"  {number}. {alarm}")
                # Print the edit options
                print("\n  1. Add an alarm")
                # Print edit option 2
                print("  2. Change an alarm's time")
                # Print edit option 3
                print("  3. Remove an alarm")
                # Print edit option 4
                print("  4. Turn one alarm ON/OFF")
                # Print edit option 5
                print("  5. Change the days this list rings on")
                # Print edit option 6
                print("  6. Back to the main menu")
                # Ask the user for their choice and remove extra spaces
                choice = self.ask("\nChoose an option: ").strip()

                # If the user chose 1 (add an alarm)
                if choice == "1":
                    # Ask for the new time and keep only the time part
                    new_time = self.ask_time("New alarm time (HH:MM): ").time()
                    # If there is already an alarm at that time
                    if chosen.has_time(new_time):
                        # Set a message explaining why nothing was added
                        message = "There is already an alarm at that time."
                    # If the time is free
                    else:
                        # Add the alarm to the list
                        chosen.add_alarm(new_time)
                        # Save the change to the file
                        self.file_manager.save_to_file(self.alarm_lists)
                        # Set a message to confirm it worked
                        message = f"Added an alarm at {new_time.strftime(TIME_FORMAT)}."
                        # If the user chose 2 (change a time)
                    elif choice == "2":
                    # Let the user pick which alarm to change
                    alarm = self.choose_alarm(chosen)
                    # Ask for the new time and keep only the time part
                    new_time = self.ask_time("New time (HH:MM): ").time()
                    # If there is already an alarm at that time
                    if chosen.has_time(new_time):
                        # Set a message explaining why nothing changed
                        message = "There is already an alarm at that time."
                    # If the time is free
                    else:
                        # Give the alarm its new time
                        alarm.time = new_time
                        # Put the alarms back in order
                        chosen.sort_alarms()
                        # Save the change to the file
                        self.file_manager.save_to_file(self.alarm_lists)
                        # Set a message to confirm it worked
                        message = f"Changed the alarm to {new_time.strftime(TIME_FORMAT)}."
                    # If the user chose 3 (remove an alarm)
                elif choice == "3":
                    # A list must keep at least one alarm (an empty list cannot be saved)
                    if len(chosen.alarms) == 1:
                        # Tell the user what to do instead
                        message = "A list needs at least one alarm. Use 'Delete a list' instead."
                    # If the list has more than one alarm
                    else:
                        # Let the user pick which alarm to remove
                        alarm = self.choose_alarm(chosen)
                        # Remove it from the list
                        chosen.alarms.remove(alarm)
                        # Save the change to the file
                        self.file_manager.save_to_file(self.alarm_lists)
                        # Set a message to confirm it worked
                        message = f"Removed the alarm at {alarm.time.strftime(TIME_FORMAT)}."
                    # If the user chose 4 (turn one alarm ON/OFF)
                elif choice == "4":
                    # Let the user pick which alarm to switch
                    alarm = self.choose_alarm(chosen)
                    # Flip it: ON becomes OFF, OFF becomes ON
                    alarm.is_active = not alarm.is_active
                    # Save the change to the file
                    self.file_manager.save_to_file(self.alarm_lists)
                    # Pick the word ON or OFF for the message
                    word = "ON" if alarm.is_active else "OFF"
                    # Set a message to confirm it worked
                    message = f"The alarm at {alarm.time.strftime(TIME_FORMAT)} is now {word}."
                    # If the user chose 5 (change the days)
                elif choice == "5":
                    # Ask for the new days and save them in the list
                    chosen.days = self.ask_days()
                    # Save the change to the file
                    self.file_manager.save_to_file(self.alarm_lists)
                    # Set a message to confirm it worked
                    message = f"This list now rings: {chosen.days_text()}."
                    # If the user chose 6 (back)
                elif choice == "6":
                    # Stop repeating and leave this function
                    break
                    # If the user typed anything else
                else:
                    # Set a message asking for a valid number
                    message = "Please choose a number from 1 to 6."

                    # This is used when the user answers a ringing alarm: W = I woke up, S = snooze

def answer_alarm(self, command):
                    # If the user typed "s" (snooze)
                    if command == "s":
                        # Stop the ringing; the next alarm will ring at its own time
                        self.ringing_alarm = None
                        # Tell the user when the next alarm will ring
                        print(f"Snoozed. Next alarm: {self.next_alarm_text()}")
                    # If the user typed "w" (I woke up)
                    else:
                        # Remember the list that was ringing
                        woken_list = self.ringing_list
                        # Stop the ringing straight away
                        self.ringing_alarm = None
                        # Turn off the alarms in that list that are still to come
                        count = woken_list.i_woke_up(datetime.now().time())
                        # Save the change to the file
                        self.file_manager.save_to_file(self.alarm_lists)
                        # Tell the user how many alarms were turned off
                        print(f"Good morning! Turned off {count} remaining alarm(s) in '{woken_list.name}'.")

                    # This asks the user a question; if an alarm is ringing, W and S answer the alarm instead

def ask(self, prompt):
                    # Repeat until we have a normal answer
                    while True:
                        # Ask the question and wait for the user to type
                        text = input(prompt)
                        # Clean the answer: remove spaces and make it lowercase
                        command = text.strip().lower()
                        # If an alarm is ringing and the user typed w or s
                        if self.ringing_alarm is not None and command in ("w", "s"):
                            # Handle the alarm answer
                            self.answer_alarm(command)
                            # Go back to the top and ask the same question again
                            continue
                        # Otherwise give the answer back to whoever asked
                        return text

                    # This finds the next alarm that will really ring (it looks at each list's days)

def find_next_alarm(self):
                    # Get the current date and time
                    now = datetime.now()
                    # Start with no alarm found
                    best_alarm = None
                    # This will hold the date and time when the best alarm rings
                    best_time = None
                    # Go through every alarm list
                    for alarm_list in self.alarm_lists:
                        for alarm in alarm_list.alarms:
                            # Only look at alarms that are ON
                            if alarm.is_active:
                                # Look at today and the next 7 days
                                for days_ahead in range(8):
                                    # Work out the date that is this many days from now
                                    day = now + timedelta(days=days_ahead)
                                    # Check if the list rings on that day of the week
                                    if day.weekday() in alarm_list.days:
                                        # Join that date with the alarm's time
                                        ring_time = datetime.combine(day.date(), alarm.time)
                                        # Check that this moment is still in the future
                                        if ring_time > now:
                                            # If we have none yet, or this one is sooner than the one we have
                                            if best_time is None or ring_time < best_time:
                                                # Keep this alarm as the best one so far
                                                best_alarm = alarm
                                                # Keep its date and time too
                                                best_time = ring_time
                                            # The first matching day is enough for this alarm
                                            break
                        # Give back the alarm and when it rings (both are None if there is none)
                    return best_alarm, best_time

                    # This gives the next alarm as text, like "07:05 (School)" or "Mon 07:00 (School)"
                    def next_alarm_text(self):
                        # Find the next alarm and when it rings
                        alarm, ring_time = self.find_next_alarm()
                        # If there is no active alarm at all
                        if alarm is None:
                            # Say so
                            return "none (no active alarms)"
                        # If the alarm rings today
                        if ring_time.date() == datetime.now().date():
                            # Show only the time
                            when = ring_time.strftime(TIME_FORMAT)
                        # If the alarm rings on another day
                        else:
                            # Show the short day name and the time
                            when = ring_time.strftime("%a ") + ring_time.strftime(TIME_FORMAT)
                        # Give back the text
                        return f"{when} ({alarm.label})"

                    # This plays a sound once so the alarm can be heard
                    def play_sound(self):
                        # If this computer is a Mac
                        if sys.platform == "darwin":
                            # Play a built-in Mac sound file (the program waits until it finishes)
                            os.system("afplay /System/Library/Sounds/Glass.aiff")
                        # If this computer is Windows
                        elif sys.platform.startswith("win"):
                            # Load the Windows sound tool (only exists on Windows)
                            import winsound
                            # Play a beep at 1000 Hz for 700 milliseconds
                            winsound.Beep(1000, 700)
                        # If this is any other computer
                        else:
                            # Print the terminal bell character, which makes a beep on many terminals
                            print("\a", end="", flush=True)
                            # Wait 1 second so the beeps are not too fast
                            sleep(1)

                    # This runs in the background: it watches the real clock and starts alarms ringing
                    def watch_clock(self):
                        # Remember which alarms already rang so each one only rings once
                        already_rung = set()
                        # Keep going until the user stops the alarms
                        while self.running:
                            # Get the real current date and time from the computer
                            now = datetime.now()
                            # Turn the current time into text like "07:05" so we can compare it
                            now_text = now.strftime(TIME_FORMAT)
                            # Go through every alarm list
                            for alarm_list in self.alarm_lists:
                                # Go through every alarm in this list
                                for alarm in alarm_list.alarms:
                                    # Make a tag for this alarm on today's date (so it can ring again tomorrow)
                                    tag = (alarm_list.name, now.strftime("%Y-%m-%d"), now_text)
                                    # Check: alarm is ON, today is one of the list's days, its time matches now, and it has not rung yet
                                    if alarm.is_active and now.weekday() in alarm_list.days and alarm.time.strftime(
                                            TIME_FORMAT) == now_text and tag not in already_rung:
                                        # Remember that this alarm has rung
                                        already_rung.add(tag)
                                        # Only start ringing if no other alarm is ringing right now
                                        if self.ringing_alarm is None:
                                            # Remember which list the ringing alarm belongs to
                                            self.ringing_list = alarm_list
                                            # Remember which alarm is ringing (this starts the sound)
                                            self.ringing_alarm = alarm
                                            # Tell the user which alarm is ringing
                                            print(f"\n*** ALARM: {alarm_list.name} - {now_text} ***")
                                            # Tell the user how to answer
                                            print("Type W if you woke up, or S to snooze, then press Enter.")
                            # If an alarm is ringing
                            if self.ringing_alarm is not None:
                                # Play the sound (this repeats until the user answers)
                                self.play_sound()
                            # If nothing is ringing
                            else:
                                # Wait 1 second before checking the clock again
                                sleep(1)

                    # This starts the clock in the background, then shows the home screen until the user exits
                    def run(self):
                        # Mark the alarms as running
                        self.running = True
                        # Make the background worker; daemon=True means it stops if the program closes
                        clock_thread = threading.Thread(target=self.watch_clock, daemon=True)
                        # Start the background worker (from now on the alarms can ring on any screen)
                        clock_thread.start()
                        # Repeat forever (until we use break)
                        while True:
                            # Show the home screen with the saved lists
                            self.show_dashboard()
                            # Print the menu heading
                            print("\nMENU")
                            # Print menu option 1
                            print("  1. Create an alarm list")
                            # Print menu option 2
                            print("  2. View alarms in a list")
                            # Print menu option 3
                            print("  3. Edit a list (add, change or remove alarms)")
                            # Print menu option 4
                            print("  4. Turn a whole list ON/OFF")
                            # Print menu option 5
                            print("  5. Delete a list")
                            # Print menu option 6
                            print("  6. Exit")
                            # Ask the user for their choice and remove extra spaces
                            choice = self.ask("\nChoose an option: ").strip()

                            # If the user chose 1
                            if choice == "1":
                                # Run the create list screen
                                self.create_list()
                                # Wait for Enter before going back to the menu
                                self.pause()
                            # If the user chose 2
                            elif choice == "2":
                                # Run the view alarms screen
                                self.view_alarms()
                                # Wait for Enter before going back to the menu
                                self.pause()
                            # If the user chose 3
                            elif choice == "3":
                                # Run the edit screen (it has its own way to go back)
                                self.edit_list()
                            # If the user chose 4
                            elif choice == "4":
                                # Run the turn on/off screen
                                self.toggle_list()
                                # Wait for Enter before going back to the menu
                                self.pause()
                            # If the user chose 5
                            elif choice == "5":
                                # Run the delete screen
                                self.delete_list()
                                # Wait for Enter before going back to the menu
                                self.pause()
                            # If the user chose 6
                            elif choice == "6":
                                # Tell the background worker to stop
                                self.running = False
                                # Stop any ringing
                                self.ringing_alarm = None
                                # Say goodbye and remind the user that closed means no alarms
                                print("Goodbye! Alarms cannot ring while the program is closed.")
                                # Stop the loop, which ends the program
                                break
                            # If the user typed anything else
                            else:
                                # Tell the user to pick a valid number
                                print("Please choose a number from 1 to 6.")
                                # Wait for Enter so the message can be read
                                self.pause()

                    # This is true only when you run this file directly (not when it is imported)


if __name__ == "__main__":
    # Make the app and start the home screen
    AlarmApp().run()



















