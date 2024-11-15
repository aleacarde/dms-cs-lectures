# dms-cs-lectures

*Structure inspired by [this great haskell course](https://github.com/haskell-beginners-2022/exercises)*

*This readme is also adapted from there because I like it.*

## Working with these exercises
This section contains instructions about setting up the development environment and preparing this repository.
Exerises are in the src directory. Each module provides exercises for an individual lecture and has the corresponding name (e.g. Lecture1.py).

### First time
Fork this repository.

Enable GitHub Actions for your forked repository.

Visit: `https://github.com/<YOUR_GITHUB_USERNAME>/dms-cs-lectures/`

Clone your forked repository.

Enter your local repo directory and add the original repository as a course remote.

`git remote add course https://github.com/aleacarde/dms-cs-lectures.git`

You can verify that everything is done correctly by running the git remote -v command. The output of this command will look similar to the below:

You can verify that everything is done correctly by running the `git remote -v` command. The output of this command will look similar to the below:

```
course https://github.com/aleacarde/dms-cs-lectures.git (fetch)
course https://github.com/aleacarde/dms-cs-lectures.git (push)
origin https://github.com/<YOUR_GITHUB_USERNAME>/dms-cs-lectures.git (fetch)
origin https://github.com/<YOUR_GITHUB_USERNAME>/dms-cs-lectures.git (push)
```

## Setup for Windows

Go to the `dms-cs.code-workspace` file at the top of the project directory, delete the section that says:

`"python.defaultInterpreterPath": "./.venv/bin/python"`

and uncomment (remove the two forward-slashes at the beginning of the line) the section right under the section you just deleted. You are looking for the line that says:

`//"python.defaultInterpreterPath": ".\\.venv\\Scripts\\python.exe" // For Windows`

First, open powershell and `cd` to the top of the project directory (assuming that powershell didn't already open there).

Then run:

`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass1`

Lastly, run:

`.\setup-python-env.ps1`

### Asking for feedback
Implement your solutions in a separate branch (not main). You can run the following command to create a new branch and switch to it at the same time:

`git checkout -b lecture-1-exercises`

When you have finished implementing exercises for a particular lecture, create a Pull Request **to your fork**.

To open a PR to your fork, you need to change base repository to your own repository, as shown on the screenshot below:

PR to fork example

After you change, the PR view will change accordingly:

Final PR to fork

### Updating your fork
To get the latest updates, follow the below instructions:

Switch to your main branch locally and make sure it's in sync with the latest version of your fork on GitHub.
```
git checkout main
git pull --rebase --prune
```
Fetch all the course changes and save them locally.
```
git fetch course main
git rebase course/main
```
NOTE: This stage may require you to resolve conflicts.

Push local changes to your own fork.

`git push origin main --force`
