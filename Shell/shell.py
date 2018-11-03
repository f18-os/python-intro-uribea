#! /usr/bin/env python3

import os, sys, re, time

pid = os.getpid()


sys.ps1 = os.environ.get('PS1')

if sys.ps1 is None :
    sys.ps1 = '$ '
cmd = input(sys.ps1)
while cmd != "exit":
    allcmd = cmd.split('\n')
    for cmds in allcmd:
        r = -1
        w = -1
        b = False
        o = False
        inp = False
        path = ''
        text = cmds.split("|")
        if text[0] == '':
            continue
        elif text[0].lstrip().startswith('/'):
            text[0] = text[0].lstrip()
            #print(text[0]+'atelif')
            bcmdp = text[0].split('/')
            bcmd = bcmdp.pop()
            path = "/".join(bcmdp)
            #print(path)

        elif text[0].__contains__('cd'):
            chnd = str.split(text[0])
            cwd = ''
            if len(chnd)>1:
                if chnd[1].startswith('.'):
                    cwd = os.getcwd()
                path = cwd + '/' + chnd[1]
                os.chdir(path)
                text[:] = []
                path = ''
        i = len(text)
        for p in range(i):
            #time.sleep(.1)
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
                if len(path) > 0 and path.startswith('/'):
                    #print(path +"atpath"+bcmd)
                    program = "%s/%s" % (path, bcmd)
                    try:
                        #print(program)
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:  # ...expected
                        pass  # ...fail quietly
                    sys.exit(1)  # terminate with error

                else:
                    for dire in re.split(":", os.environ['PATH']):  # try each directory in the path
                        program = "%s/%s" % (dire, args[0])
                        #print(program + 'at fir')
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
        cmd = input(sys.ps1)
    except EOFError:
        sys.exit(1)
