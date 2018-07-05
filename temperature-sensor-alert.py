import os
import subprocess
import time
import random

from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
#go twilio and create account
account_sid = "" # put your Sid account here in ""
auth_token = '' # put your token here in ""
client = Client(account_sid, auth_token)


def check_lm_sensors():
    soft=subprocess.call(['which','sensors'])
    if soft == 0:
        print("lm_sensors is installed")
    else:
        rep=input("Do you want to install lm-sensors to good working? Y|N ?")
        if rep in ["Y","y","yes","YES"]:
            os.system("sudo apt-get install lm-sensors")
        else :
            print("Ok! Good bye! this script can't run without lm-sensors")
            time.sleep(3)
            exit()

def check_temp():
    #read value to variables
    physical = os.popen("cat /sys/class/hwmon/hwmon2/temp1_input").read()
    core0 = os.popen("cat /sys/class/hwmon/hwmon2/temp2_input").read()
    core1 = os.popen("cat /sys/class/hwmon/hwmon2/temp3_input").read()

    #cut value decimal 650000 to 65
    physical_cut = physical[0:2]
    core0_cut = core0[0:2]
    core1_cut = core1[0:2]

    #convert value string to int
    physical_int= int(physical_cut)
    core0_int = int(core0_cut)
    core1_int = int(core1_cut)

    if physical_int > 80 or core0_int > 80 or core1_int > 80:
        message = client.messages.create(
        body="Alert the server overheating\nphysical {0} C\ncore0 {1} C\ncore1 {2} C".format(physical_int,core0_int,core1_int),
        to="", #put the number or the alert will be send
        from_="" #put the phone number that twilio you to give ex :+10109620000
        )
# Main
check_lm_sensors()
while True:
    check_temp()
    time.sleep(30)
