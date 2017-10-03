<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.1.0
-->


# Managing the Git Repository and GitHub
In here are instructions on the creation, maintenance, and use of this repository
via [git][01] and [GitHub][02].  For more information, check out these posts:

* [Using Git and Github to Manage Your Dotfiles][03]
* [Managing dot files with Git][04]

Check this out:
* [git - the simple guide just a simple guide for getting started with git. no deep shit ;)](http://rogerdudler.github.io/git-guide/)
* [Git Tutorial](http://fab.cba.mit.edu/classes/4.140/doc/git/)
* [What is git?](http://fab.cba.mit.edu/classes/863.16/doc/tutorials/version_control/index.html)

================================================================================
## Creating a Git Repository

### Creating Your Remote GitHub Repository
Create a new repository on GitHub.
To avoid errors, do not initialize the new repository with README, license, or gitignore files.
You can add these files when you push your project to GitHub.

Go to [GitHub][02] and create the new repository called jupyter-notebook.

    goto https://github.com/jupyter-notebooks

### Creating Your Local Git Repository
On your system where your project is located,
open a terminal and change the current working directory to your local project.

Change to the `jupyter-notebooks` directory, and initialize it as a git repository

    cd ~/jupyter-notebooks
    git init

Add all your source files, create a `README.md` file
and create the file `.gitignore` like this:

    ### ------------------------- Project Specific ------------------------- ###

    ### Videos & Images ###
    *.mp4
    *.avi
    *.png
    *.jpg
    *.tif
    *.gif

    ### ----------------------------- General ------------------------------ ###

    ### Compiled Source ###
    *.pyc
    *.com
    *.class
    *.dll
    *.exe
    *.o
    *.so

    ### Packages ###
    *.7z
    *.dmg
    *.gz
    *.iso
    *.jar
    *.rar
    *.tar
    *.zip

    ### Logs & Databases ###
    *.log
    *.sql
    *.sqlite

    ### OS Generated Files ###
    *.out
    *.swp
    .DS_Store
    .DS_Store?
    ._*
    .Spotlight-V100
    .Trashes
    Icon?
    ehthumbs.db
    Thumbs.db

Now commit all these files to the git repository:

    git add --all
    git commit -m 'Initial creation of jupyter-notebooks'

### Update the Remote GitHub Repository for the First Time
Initialize the local directory as a Git repository.
Within the `jupyter-notebooks` directory, use `git` to load the files to GitHub

#### Store Credentials Within Git
To add a new remote,
use the `git remote add` command on the terminal,
in the directory your repository is stored at.

    cd ~/jupyter-notebooks

    # set your remote repository URL
    git remote add origin https://github.com/jeffskinnerbox/jupyter-notebooks.git

    # verifies the new remote URL
    git remote -v

    # pushes the changes in your local repository up to the remote repository
    git push -u origin master

>**NOTE**: Other operations
[rename an existing remote](https://help.github.com/articles/renaming-a-remote/),
[delete an existing remote](https://help.github.com/articles/removing-a-remote/).

================================================================================
## Updating a Git Repository

### Updating the Local Git Repository
Within the .vim directory, do a "get status" to see what will be included in the commit,
add files (or remove) that are required, and then do the commit to the local git repository.

    git status
    git add --all
    git commit --dry-run
    git commit -m <comment>

### Retrieving Update From Remote Repository (i.e. GitHub)
To retrieve these updates on another system, use

    git pull origin master

To overwrite everything in the local directory

    git fetch --all
    git reset --hard origin/master

Explanation: `git fetch` downloads the latest from remote without trying to merge or rebase anything.
Then the `git reset` resets the master branch to what you just fetched.
The `--hard` option changes all the files in your working tree to match the files in `origin/master`.
If you have any files that are _not_ tracked by Git,
these files will not be affected.

### Updating the Remote Repository (i.e. GitHub)
To which shows you the URL that Git has stored for the shortname for
the remote repository (i.e. GitHub):

    git remote -v

Now to push your files to the GitHub repository

    git push -u origin master

================================================================================
## Cloning a Git Repository

### Clone This Git Repository
Copy this Git repository into your local systems:

    cd <target-directory>
    git clone http://github.com/jeffskinnerbox/jupyter-notebooks.git

### Retrieving Update From Remote Repository (i.e. GitHub)
To retrieve these updates on another system, use

    git pull origin master

To overwrite everything in the local directory

    git fetch --all
    git reset --hard origin/master

Explanation: `git fetch` downloads the latest from remote without trying to merge or rebase anything.
Then the `git reset` resets the master branch to what you just fetched.
The `--hard` option changes all the files in your working tree to match the files in `origin/master`.
If you have any files that are _not_ tracked by Git,
these files will not be affected.

================================================================================
# References



[01]:http://git-scm.com/
[02]:https://github.com/
[03]:http://blog.smalleycreative.com/tutorials/using-git-and-github-to-manage-your-dotfiles/
[04]:http://blog.sanctum.geek.nz/managing-dot-files-with-git/
