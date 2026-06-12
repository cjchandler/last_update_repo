#example control script
from last_update_pusher import *
while True: 
    time.sleep(1)
    #do controls stuff etc
    
    push_latest_timestamp_if_needed( "/home/cjchandler/Git_Projects/last_update_repo/" , "mike_desktop_online.txt" , 60*2 )
    
