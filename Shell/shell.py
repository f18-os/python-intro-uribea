#! /usr/bin/env python3

import os, sys, re, time

pid = os.getpid()
# text = ''
cmd = input("$ ")
while cmd != "exit":
    r = -1
    w = -1
    b = False
    o = False
    inp = False
    text = cmd.split("|")
    #print(text)
    i = len(text)
    for p in range(i):
        time.sleep(1)
        child = text[0]
        args = str.split(child)
        if len(text) > 1:
            #print("leng > 1")
            #print(text)
            r, w = os.pipe()
            # rc = os.fork()
            del text[0]
            #print(text)
            b = True
        #print(args)
        #os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

        rc = os.fork()

        if rc < 0:
            #os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:  # child
            #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
            #             (os.getpid(), pid)).encode())

            # args = ["wc", "shell.py"]
            #print(args)

            if '>' in args:
                o = True
                os.close(1)  # redirect child's stdout
                i = args.index('>')  # print(i)
                del args[i]  #print(args)            #os.write(2, ("%d\n" % len(args)).encode())            #os.write(2, ("%s \n" % args[i]).encode())
                sys.stdout = open(args[i], "w")
                args = args[:i]
                fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                os.set_inheritable(fd, True)
                #os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())  # args = re.split(" ", input("/>"),1)

            elif '<' in args:
                inp = True
                #print("why dough")
                os.close(0)  # redirect child's stdin
                i = args.index('<')
                del args[i]
                #print(args)
                sys.stdin = open(args[i], "r")
                args = args[:i]
                fd = sys.stdin.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                os.set_inheritable(fd, True)  # args = sys.stdin.read().split()
             #   os.write(2, ("Child: opened fd=%d for reading\n" % fd).encode())

            if b and not child in text[0] and not o:
                #del text[0]
                #print(child)
                #print(True)
                #print(r)
                #print(w)
                #print(text)
                os.close(r)  # redirect child's stdout
                #sys.stdout = r#open(w, "w")
                fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                os.dup2(w,fd)
                #os.set_inheritable(fd, True)
                #os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())  # args = re.split(" ", input("/>"),1)
            elif b and child in text and text.index(child)==0 and not inp:
                #print(child)
                os.close(w)  # redirect child's stdin
                #sys.stdin = open(r, "r")
                fd = sys.stdin.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                os.dup2(r,fd)
                #os.set_inheritable(fd, True)  # args = sys.stdin.read().split()
                #os.write(2, ("Child: opened fd=%d for reading\n" % fd).encode())

            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, args[0])  # os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
                try:
                    os.execve(program, args, os.environ)  # try to exec program
                except FileNotFoundError:  # ...expected
                    pass  # ...fail quietly

            #os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
            sys.exit(1)  # terminate with error

        #else:  # parent (forked ok)
         #   os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
          #              (pid, rc)).encode())
    for p in range(i):
        childPidCode = os.wait()
        try:
            os.close(r)
            os.close(w)
        except OSError:  # ...expected
            pass
        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
        #             childPidCode).encode())
    cmd = input("$ ")
