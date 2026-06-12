#last_update_pusher

import os
import time
import subprocess

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
    
    #when did it last push a git commit to github? it would be on the last commit, so check that: 

    
    # Run the command and capture its output
    result = subprocess.run(["git", "log", "-1", "--format=%ct"], capture_output=True, text=True, cwd= path_to_last_update_repo)
    tpush = result.stdout.strip()
    
    last_push_timestamp = float(tpush)
    print("last push was at : ",last_push_timestamp) 
    print("next push is at :", last_push_timestamp + push_interval_sec)
    print("time until next push : " ,last_push_timestamp + push_interval_sec - tnow)

    
    #push if needed now
    if( tnow > last_push_timestamp + push_interval_sec):
        push_latest_timestamp(path_to_last_update_repo , project_name_txt)

#push_latest_timestamp_if_needed( "/home/cjchandler/Git_Projects/last_update_repo/" , "mike_desktop_online.txt" , 10)
