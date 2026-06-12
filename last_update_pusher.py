#last_update_pusher

import os
import time

def push_latest_timestamp( path_to_last_update_repo , project_name_txt ): 
    tnow = time.time() 
    
    #update the project file with current time
    f = open( path_to_last_update_repo + project_name_txt, "w")
    f.write(str(tnow))
    f.close()
    
    #push that to git
    os.system('cd '+ path_to_last_update_repo + ' \n git pull origin main --no-edit --allow-unrelated-histories') #the no-edit is so it merges automatically 
    
    os.system( 'cd '+ path_to_last_update_repo + ' \n git add . \n  git commit -a -m "data_automatic" ')
            
    os.system('cd '+ path_to_last_update_repo + ' \n git push origin main')
    print("backup via git is done")


def push_latest_timestamp_if_needed( path_to_last_update_repo , project_name_txt , push_interval_sec ):
    tnow = time.time()
    #update the project file with current time
    f = open( path_to_last_update_repo + project_name_txt, "w")
    f.write(str(tnow))
    f.close()
    
    #look at the last time we pushed
    with open(path_to_last_update_repo + project_name_txt, "r", encoding="utf-8") as file:
        timestampstr = file.read()
        last_push_timestamp = float(timestampstr)
    
    #push if needed now
    if( tnow > last_push_timestamp + push_interval_sec):
        push_latest_timestamp(path_to_last_update_repo , project_name_txt)

