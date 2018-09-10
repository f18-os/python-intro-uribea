#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()
#text = ''
dire = re.split(":", os.environ['PATH'])
dire = dire[0]
text = input(dire + "> ")
while text!="q":

    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())

        #args = ["wc", "shell.py"]
        args = re.split(" ", text, 1)
        print(args)
        if args[0]=='>':
            os.close(1)  # redirect child's stdout
            sys.stdout = open(args[1], "w")
            fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
#            args = re.split(" ", input("/>"),1)

        elif args[0]=='<':
            os.close(0)  # redirect child's stdin
            sys.stdin = open(args[1], "r")
            fd = sys.stdin.fileno()  # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            args = sys.stdin.read().split()
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args, os.environ) # try to exec programwai
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                     childPidCode).encode())
        text = input(dire[0] + "> ")
