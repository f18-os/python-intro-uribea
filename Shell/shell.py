#! /usr/bin/env python3

import os, sys, re, time

pid = os.getpid()
try:
    cmd = input(sys.ps1)
except:
    cmd = input("$ ")

while cmd != "exit":
    r = -1
    w = -1
    b = False
    o = False
    inp = False
    text = cmd.split("|")

    if text[0].__contains__('cd'):
        chnd = str.split(text[0])
        cwd = ''
        if chnd[1].startswith('.'):
            cwd = os.getcwd()
        path = cwd + '/' + chnd[1]
        os.chdir(path)
        text[:] = []
    i = len(text)
    for p in range(i):
        time.sleep(.1)
        child = text[0]
        args = str.split(child)
        if len(text) > 1:
            r, w = os.pipe()
            del text[0]
            b = True

        rc = os.fork()

        if rc < 0:
            sys.exit(1)

        elif rc == 0:  # child

            if '>' in args:
                o = True
                os.close(1)
                i = args.index('>')
                del args[i]
                sys.stdout = open(args[i], "w")
                args = args[:i]
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)

            elif '<' in args:
                inp = True
                os.close(0)
                i = args.index('<')
                del args[i]
                sys.stdin = open(args[i], "r")
                args = args[:i]
                fd = sys.stdin.fileno()
                os.set_inheritable(fd, True)

            if b and not child in text[0] and not o:
                os.close(r)
                fd = sys.stdout.fileno()
                os.dup2(w,fd)
            elif b and child in text and text.index(child)==0 and not inp:
                os.close(w)
                fd = sys.stdin.fileno()
                os.dup2(r,fd)

            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)  # try to exec program
                except FileNotFoundError:  # ...expected
                    pass  # ...fail quietly

            sys.exit(1)  # terminate with error

    for p in range(i):
        childPidCode = os.wait()
        try:
            os.close(r)
            os.close(w)
        except OSError:  # ...expected
            pass
    try:
        try:
            cmd = input(sys.ps1)
        except:
            cmd = input("$ ")

    except EOFError:
        sys.exit(1)
