import subprocess as sp
import os
import time
import pandas as pd
import csv
import collections
import datetime
from twilio.rest import Client
import sys
import select
import numpy as np


import os
from twilio.rest import Client



def send_message( message_string):
    path = "/home/carl/Desktop/"
    filename = "twiliokey.txt"
    f = open(path + filename, "r")
    sid_string = (f.readline())
    auth_string = (f.readline())

    print(sid_string.rstrip())
    print(auth_string.rstrip())

    TWILIO_ACCOUNT_SID = sid_string.rstrip()
    TWILIO_AUTH_TOKEN = auth_string.rstrip()
    twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


    try:
        message = client.messages.create(
        from_='+19854974121',
        body=message_string,
        to='+19023077435')
        return 0

    except:
        print("twillo not working")
        return 1





def parse_incoming_texts():

    path = "/home/carl/Desktop/"
    filename = "twiliokey.txt"
    f = open(path + filename, "r")
    sid_string = (f.readline())
    auth_string = (f.readline())


    TWILIO_ACCOUNT_SID = sid_string
    TWILIO_AUTH_TOKEN = auth_string
    twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    smslist = twilio_api.messages.stream()
    direction = "nan"
    timestamp= -1
    for x in smslist:
        if(x.direction == 'inbound'):
            #get the most recent message that I texted to twilio number
            print( x.date_sent.timestamp() )
            print( x.direction)
            timestamp = x.date_sent.timestamp()
            try:
                partslist =  x.body.split(' ')
                if partslist[0] == 'Stop':
                    return float(partslist[1]) , timestamp
                if partslist[0] == 'Reset':
                    return 0 , timestamp
            except:
                send_message("I can't parse the last text command you sent, try again")
                return 0 , timestamp






class basic_monitor: #this looks at a time file and sends alarm itf it's been too long without updates
    def __init__(self , filein , check_sec): #check sec is how many seconds without updates is ok
        # ~ if os.path.isdir('last_update_repo') == False:
            # ~ print("cloning the last update repo git archive , it's public ")
            # ~ os.system('git clone https://github.com/cjchandler/last_update_repo.git')
        # ~ else:
            # ~ print("pull the latest version")
            # ~ os.system("cd last_update_repo \n git pull origin main")
        self.filename = filein
        self.backup_interval = check_sec

        self.alarms_active_dict = {}
        self.alarm_last_send_dict= {}
        self.alarm_next_send_dict= {}
        self.alarm_message_dict= {}

        self.alarms_active_dict['git alarm'] = False
        self.alarms_active_dict['file update alarm'] = False


        self.alarm_last_send_dict['file update alarm'] = 0



        self.alarm_next_send_dict['file update alarm'] = 0


        self.last_backup_time = 0


    def pull_through_git(self ):

        if( True):

            try:
                os.system("cd ./ \n git pull origin main")
                self.last_backup_time = time.time()
                self.alarms_active_dict['git alarm'] = False
                print("backup via git is gotten")


            except:
                print("failed to get data updates via git")
                self.alarms_active_dict['git alarm'] = True
                # ~ self.git_alarm.sound_alarm( "could not pull git to server " + time.ctime() )

    def file_updated_recently(self):
        f = open("./" + self.filename, "r")
        dstring = (f.readline())
        if time.time() > float(dstring) + self.backup_interval:
            return False, float(dstring)
        else :
            return True, float(dstring)


    def look_at_data_update_alarm_states(self):
        recent_file_update_bool, self.last_backup_time  = self.file_updated_recently()


        #reset all alarms to off
        for key in self.alarms_active_dict:
             self.alarms_active_dict[key] = 0

        #now check if any alarms are active from the current data set

        time_since_last_save = time.time() - int(self.last_backup_time )

        if( time_since_last_save >=  self.backup_interval     ):
            self.alarms_active_dict['file update alarm'] = True
            self.alarm_message_dict[  'file update alarm'] = self.filename+ " not logging data in last update repo. secs without data = "+ str(time_since_last_save) +"  Probably malfunctioning seriously "

            print( "no file updates in " , time_since_last_save , "seconds")


    def send_alarms(self):
        #look at all active alarms
        for key in self.alarms_active_dict:
            if self.alarms_active_dict[key] == True:
                #look at the last time we sent an alatm
                last_alarm =  self.alarm_last_send_dict[key]
                #look at the next alarm send time:
                next_alarm = self.alarm_next_send_dict[key]

                #if past next alarm time, send it, update last send
                if time.time() > next_alarm:
                    print("sent and alarm for " , key)
                    send_message( self.filename + key + " " + self.alarm_message_dict[key] + "  " + time.ctime() + "GMT, this is server alarm" )
                    self.alarm_last_send_dict[key] = time.time()


    def check_incoming_messages(self):
        hrs_alarm_paused, incoming_timestamp = parse_incoming_texts()
        print( "last incoming text was at " , incoming_timestamp , " with hrs pause = " , hrs_alarm_paused)
        #look at all active alarms
        for key in self.alarms_active_dict:
            if self.alarms_active_dict[key] == True:
                self.alarm_next_send_dict[key] = incoming_timestamp + hrs_alarm_paused*60*60


    def do_all(self):

        self.pull_through_git()
        self.look_at_data_update_alarm_states()
        self.check_incoming_messages()
        self.send_alarms()



#sm = server_monitor("today_data.csv")
#smv2 = server_monitor("today_dataV2.csv" , True)
#smv4 = server_monitor("today_dataV4.csv" , False)


growth_chamber = basic_monitor( "hoz_tomatoes.txt" , 60*10)#10 min delay
incubator_v4 = basic_monitor( "incubator_v4.txt" , 60*7)
incubator_v2 = basic_monitor( "incubator_v2.txt" , 60*7)

while True:
    growth_chamber.do_all()
    incubator_v4.do_all()
    incubator_v2.do_all()
    print("sleeping- last repo monitor that all files are being updated")
    time.sleep(60)
