# Banshee [![Build Status](https://travis-ci.org/NWChen/banshee.svg?branch=master)](https://travis-ci.org/NWChen/banshee)

Banshee is a tool we're developing for the 1st Information Operations Command (LAND) of the U.S. Army as part of Columbia University's [Hacking 4 Defense](http://www.h4d.cs.columbia.edu) initiative.

## Team Members
Ori Aboodi, oda2102
Zach Boughner, ztb2003
Neil Chen, nwc2112
Alan Hytonen, ajh2217
Peter Richards, pfr2109

## How do I contribute to this codebase?
If you've been added as a contributor to the project, follow these guidelines:

### First time contributing to this repo
```bash
git clone https://github.com/NWChen/banshee.git
git status
```
After you've made your changes,
```bash
git add <name of file/dir you changed>
git commit
git push origin master
```

### Not my first time
If you're making changes to an existing feature, switch to the appropriate feature branch using `git checkout <name of branch>`. If you're developing a new feature (e.g. a new scraper module), the following is recommended:
```bash
git checkout -b <name of feature>
git add <name of file/dir you changed>
git commit
git push
```
