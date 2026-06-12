# last_update_repo

Plan: 
We have scripts / controls that need 100% uptime, and I need an alarm if they stop. This repo has a file for each project or process.
The control program logs the current timestamp in a file. 
Example: lifesupport.txt is a file with a single timestamp in it. It gets updated every 10s on the computer it's running on. raspberry pi, laptop etc. 
Then there is another script that is last_update_pusher.py. 
This pulls the last_update_repo from git hub, commits the new lifesupport.txt file, then pushes it back to github. It does this every 3 min or so
last_update_pusher.py has a function in it, so you can integrate that into a python control script too, that way if the controls are running, it's pushing data to git hub

There is a server script called update_monitor_sms.py and update_monitor_slack.py. These are designed to run on servers ( I use python anywhere) and if there is no update for 5 min, they send an alarm to my phone on slack or sms
 
 



#other useful stuff: 
Deleting the .git folder may cause problems in your git repository. If you want to delete all your commit history but keep the code in its current state, it is very safe to do it as in the following:

Checkout

git checkout --orphan latest_branch

Add all the files

git add -A

Commit the changes

git commit -am "commit message"

Delete the branch

git branch -D master

Rename the current branch to master

git branch -m master

Finally, force update your repository

git push -f origin master

PS: this will not keep your old commit history around.
