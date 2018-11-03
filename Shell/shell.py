#! /usr/bin/env python3

import os, sys, re, time

pid = os.getpid()


sys.ps1 = os.environ.get('PS1')

if sys.ps1 is None :
    sys.ps1 = '$ '
cmd = input(sys.ps1)
while cmd != "exit":
    cmd = cmd.lstrip().rstrip()
    if not cmd == '':
        cmds = cmd#dont modify cmd
        r = -1#read
        w = -1#write
        b = False#fork
        o = False#output redirect
        inp = False#input redirect
        path = ''#init path
        text = cmds.split("|")#split at forks

        if text[0].__contains__('cd'):  # change directory
            chnd = str.split(text[0])
            cwd = ''
            if len(chnd) > 1:
                if chnd[1].startswith('.'):  # start at this directory
                    cwd = os.getcwd()
                path = cwd + '/' + chnd[1]
                os.chdir(path)
                text[:] = []
                path = ''

        i = len(text)#number ofr forks,
        for p in range(i):
            #if cmds == '':
            #    continue

            #time.sleep(.1)
            child = text[0]
            args = str.split(child)#arguments of current working command


            if len(text) > 1:#check if need pipe
                r, w = os.pipe()
                del text[0]#basically pop first command
                b = True

            rc = os.fork()

            if rc < 0:
                sys.exit(1)

            elif rc == 0:  # child

                if '>' in args:#check for output redirect and redirect output
                    o = True
                    os.close(1)
                    i = args.index('>')
                    del args[i]
                    sys.stdout = open(args[i], "w")
                    args = args[:i]
                    fd = sys.stdout.fileno()
                    os.set_inheritable(fd, True)

                elif '<' in args:#if input redirect redirect input
                    inp = True
                    os.close(0)
                    i = args.index('<')
                    del args[i]
                    sys.stdin = open(args[i], "r")
                    args = args[:i]
                    fd = sys.stdin.fileno()
                    os.set_inheritable(fd, True)

                if b and not child in text[0] and not o :#check if fork exists and not output redirection
                    os.close(r)
                    fd = sys.stdout.fileno()
                    os.dup2(w,fd)

                elif b and child in text and text.index(child)==0 and not inp:#check if fork and not input redirection
                    os.close(w)
                    fd = sys.stdin.fileno()
                    os.dup2(r,fd)

                if child.startswith('/'):#execute command with fullpathname

                    program = (args[0])#"%s/%s" %

                    try:
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:  # ...expected
                        pass  # ...fail quietly
                    sys.exit(1)  # terminate with error

                else:
                    for dire in re.split(":", os.environ['PATH']):  # try each directory in the path
                        program = "%s/%s" % (dire, args[0])
                        try:
                            os.execve(program, args, os.environ)  # try to exec program
                        except FileNotFoundError:  # ...expected
                            pass  # ...fail quietly

                    sys.exit(1)  # terminate with error

        for p in range(i):
            if not cmd.rstrip().endswith('&'):#if not background
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
