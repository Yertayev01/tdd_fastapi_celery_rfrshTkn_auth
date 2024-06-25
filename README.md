TDD + FASTAPI + CELERY + AUTH( REFRESH TOKEN)



git fetch origin  # Fetch the latest changes from the remote
git pull origin main  # Pull the changes into your local repository

#GITHUB push 
echo "# a" >> README.md 
git init 
git add README.md 
git commit -m "first commit" 
git branch -M main 
git remote add origin https://github.com/Yertayev01/a.git 
git push -u origin main 

#GITHUB pull 
git remote -v 
git branch -a 
git fetch origin 
git checkout <branch_name> 
git merge origin/<branch_name>