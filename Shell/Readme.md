This repository contains a python shell with limited capabilities

The shell is 

`$ shell.py` 

The shell can handle
* input redirection
* output redirection
* singular pipe
* redirection and piping
* changing directory

When piping the program creates two children otherwise only one is created(c2) for when to open and closing pipes

The progrmam uses booleans to check for pipes and priority

Changing directory is done outside of the child

Uses for loops to create childs
uses for loop to wait for children(c1)

Does not have else for parent, 
Parent has for loop that waits for all children to finish

Tried PS1 var check but failed, errors still exist when being compared on testShell.sh
