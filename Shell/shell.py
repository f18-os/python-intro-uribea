#! /usr/bin/env python3

import os, sys, re

pid = os.getpid()
#text = ''
text = input("$ ")
while text!="exit":
    args = str.split(text)
    print(args)
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())

        #args = ["wc", "shell.py"]
        print(args)
        if '>' in args:
            os.close(1)  # redirect child's stdout
            i = args.index('>')
            # print(i)
            del args[i]
            # print(args)
            #os.write(2, ("%d\n" % len(args)).encode())
            #os.write(2, ("%s \n" % args[i]).encode())
            sys.stdout = open(args[i], "w")
            args = args[:i]
            fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
            #            args = re.split(" ", input("/>"),1)

        elif '<' in args:
            print("why dough")
            os.close(0)  # redirect child's stdin
            i = args.index('<')
            del args[i]
            sys.stdin = open(args[i], "r")
            args = args[:i]
            fd = sys.stdin.fileno()  # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            #args = sys.stdin.read().split()
            os.write(2, ("Child: opened fd=%d for reading\n" % fd).encode())
        if False:
            args = ["wc", "shell.py"]
            print(args)
            os.close(1)  # redirect child's stdout
            sys.stdout = open("p4-output.txt", "w")
            fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
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
        text = input("$ ")
