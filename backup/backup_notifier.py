#!/bin/python3
""" Script to remember you to do your backups.
    This program use python-gtk to send notifications to the user's gnome
    shell.

    The only thing this script requiere is a text file containing the last
    backup date as the last line, located in /var/log and named last_backup.
    Obviously the file has to be readable for the user who want to use this
    script.

    The date has to be formatted like that: dd/mm/yyyy-hh:mm:ss
    Formatting date with bash is easy! To display the current date formatted
    for this program the command is:
    $ date +%d/%m/%Y-%H:%M:%S

    Author: Julien Delplanque
"""
from gi.repository import Notify
from datetime import datetime
from datetime import timedelta
import time

GREETING = "Hi master,"
SAY_GOODBYE = "Sincerly,\nYour Operating System"
SLEEP_TIME = 3600 # 1h

def message_and_urgency(difference: timedelta):
    """ Return a string containing a message and an Urgency according to the
        difference of time.

        Keyword arguments:
        difference - a timedelta difference of time
    """
    message = GREETING + "\n\n"
    urgency = Notify.Urgency.NORMAL
    if difference > timedelta(hours=12) and difference < timedelta(hours=24):
        message += "No backup since more than 12 hours...\n" + \
                    "It's fine but if you have time, a backup would be great. :)"
    elif difference >= timedelta(hours=24) and difference < timedelta(days=2):
        message += "No backup since more than 24 hours," + \
                   "please consider to do one. ;)"
    elif difference >= timedelta(days=2) and difference < timedelta(days=5):
        message += "No backup since more than 2 days," + \
                   "please do one, it gets dangerous!"
        urgency = Notify.Urgency.LOW
    elif difference >= timedelta(days=5):
        message += "No backup since more than 5 days, DO ONE RIGHT NOW!"
        urgency = Notify.Urgency.CRITICAL
    else:
        message += "The last backup has been done in the last 12 hours.\n" + \
                   "So it's ok. :)"
    return message + "\n\n"+SAY_GOODBYE, urgency

def last_backup_datetime():
    """ Read the file /var/log/last_backup and return the date of the last backup
        (last line) as a datetime object.
    """
    with open("/var/log/last_backup", "r") as backup_log_file:
        string_date = backup_log_file.readlines()[-1]
        return datetime.strptime(string_date, "%d/%m/%Y-%H:%M:%S\n")

def main():
    """ Main function of this program.
    """
    first_iteration = True
    Notify.init("Backup notifier")
    notification = Notify.Notification()
    while True:
      difference = datetime.today() - last_backup_datetime()
      if first_iteration or difference >= timedelta(hours=24):
          message, urgency = message_and_urgency(difference)
          notification.update("Backup notifier", message)
          notification.set_urgency(urgency)
          notification.show()
          first_iteration = False
      time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
