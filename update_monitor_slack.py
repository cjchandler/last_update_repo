import requests
import json
import os
import time



class slack_sender:
    def __init__(self):
        try:

            # Define email sender and receiver


            self.webhook_url_path = "./slackwebhookurl.txt"
            self.webhook_url = ""
            with open(self.webhook_url_path, 'r', encoding='utf-8') as f:
                    self.webhook_url = f.read()
                    self.webhook_url = self.webhook_url.strip()
                    print(self.webhook_url)

        except:
            print("couldn't load webhook url")
            quit()

    def send_message( self, body):

        message_data = {
            "text": body
        }

        response = requests.post(
            self.webhook_url,
            data=json.dumps(message_data),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")



SS = slack_sender()

#SS.send_message("testos")

#now see if the last update on v4 is recent

class basic_monitor: #this looks at a time file and sends alarm itf it's been too long without updates
    def __init__(self , filein , backup_interval): #backup_interval is how many seconds without updates is ok
        if os.path.isdir('last_update_repo') == False:
            print("cloning the last update repo git archive , it's public ")
            os.system('git clone https://github.com/cjchandler/last_update_repo.git')
        else:
            print("pull the latest version")
            os.system("cd last_update_repo \n git fetch origin")
            os.system("cd last_update_repo \n git reset --hard origin/main")


        self.filename = filein
        self.backup_interval = backup_interval

        self.alarms_active_dict = {}
        self.alarm_last_send_dict= {}
        self.alarm_next_send_dict= {}
        self.alarm_message_dict= {}

        self.alarms_active_dict['git alarm'] = False
        self.alarms_active_dict['file update alarm'] = False
        self.alarm_last_send_dict['file update alarm'] = 0
        self.alarm_next_send_dict['file update alarm'] = 0


        self.last_backup_time = 0


        self.SS = slack_sender()






    def pull_through_git(self ):

        if( True):

            try:
                os.system("cd last_update_repo \n git pull origin main")
                self.last_backup_time = time.time()
                self.alarms_active_dict['git alarm'] = False
                print("backup via git is gotten")


            except:
                print("failed to get data updates via git")
                self.alarms_active_dict['git alarm'] = True
                self.alarm_message_dict[  'git alarm'] = self.filename+ "error getting the last update repo from github"

    def file_updated_recently(self):
        f = open("./last_update_repo/" + self.filename, "r")
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
                #look at the last time we sent an alarm
                last_alarm =  self.alarm_last_send_dict[key]
                #look at the next alarm send time:
                next_alarm = self.alarm_next_send_dict[key]

                #if past next alarm time, send it, update last send
                if time.time() > next_alarm:
                    print("sent and alarm for " , key)
                    self.SS.send_message( "PYTHONANYWHERE SERVER:" + self.filename +" "+ key + " " + self.alarm_message_dict[key] + "  " + time.ctime() + "GMT, this is server alarm" )
                    self.alarm_last_send_dict[key] = time.time()



    def do_all(self):

        self.pull_through_git()
        self.look_at_data_update_alarm_states()
        self.send_alarms()


#incubator_v4 = basic_monitor( "incubator_v4.txt" , 60*4)
incubator_v2 = basic_monitor( "incubator_v2.txt" , 60*4)
incubator_VDP = basic_monitor( "incubator_VDP.txt" , 60*4)
#test_mike = basic_monitor( "mike_desktop_online.txt" , 60*4)
#incubator_v5a = basic_monitor( "incubator_v5a.txt" , 60*4)


while True:
    #incubator_v4.do_all()
    incubator_v2.do_all()
    incubator_VDP.do_all()
    #test_mike.do_all()
    #incubator_v5a.do_all()
    print("sleeping, all checks done for now")
    time.sleep(60)

