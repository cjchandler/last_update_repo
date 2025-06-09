import os
import time

def add_commit_push_through_git( last_backup_time,  backup_interval):
    backedup = last_backup_time

    if( time.time() > last_backup_time + backup_interval):
        
        try:
            
            f = open("/home/carl/Git_Projects/last_update_repo/mini_inflate.txt", "w")
            f.write(str(time.time()))
            f.close()
            os.system('cd /home/carl/Git_Projects/last_update_repo \n git pull origin main --no-edit')

            os.system( 'cd /home/carl/Git_Projects/last_update_repo \n git add . \n  git commit -a -m "data_automatic" ')
            
            os.system('cd /home/carl/Git_Projects/last_update_repo \n git push origin main')
            print("backup via git is done")
            
            backedup = time.time()
        except:
            print("didn't commit to git")


       
            
    return backedup


last_backup_time = 0 
backup_interval = 3*60 
while True: 
    last_backup_time = add_commit_push_through_git( last_backup_time,  backup_interval)
    time.sleep(10)
