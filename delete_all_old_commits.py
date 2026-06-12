#Deleting the .git folder may cause problems in your git repository. If you want to delete all your commit history but keep the code in its current state, it is very safe to do it as in the following:

#Checkout
import os
os.system('git checkout --orphan latest_branch')

#Add all the files

os.system('git add -A')

#Commit the changes

os.system('git commit -am "commit message"')

#Delete the branch

os.system('git branch -D main')

#Rename the current branch to main

os.system('git branch -m main')

#Finally, force update your repository

os.system('git push -f origin main')

#PS: this will not keep your old commit history around.
