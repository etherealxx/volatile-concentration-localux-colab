import os, subprocess, sys, shlex, pickle

curdir = '/content'
branch = '-b uiupdate+aria ' #'-b ariacivitnew ' <-space in the end
linetoexecute = [
    'git clone -b v2.1 https://github.com/camenduru/stable-diffusion-webui /content/volatile-concentration-localux', 
    f'git clone {branch}https://github.com/etherealxx/batchlinks-webui /content/volatile-concentration-localux/extensions/batchlinks-webui'
    ]

def rulesbroken(codetoexecute, cwd=''):
    global curdir
    for line in codetoexecute:
        line = line.strip()
        try:
            if curdir:
                print("[1;32m" + line)
                print('[0m')
                splittedcommand = shlex.split(line)
                # subprocess.run(line, shell=True, check=True, cwd=curdir)
                process = subprocess.Popen(splittedcommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd=curdir)
                while True:
                    # Read the output from the process
                    nextline = process.stdout.readline()
                    if nextline == '' and process.poll() is not None:
                        break
                    # Check if the line contains progress information
                    else:
                        if "%" in nextline.strip():
                            stripnext = nextline.strip()
                            print("\r", end="")
                            print(f"\r{stripnext}", end='')
                        else:
                            print(nextline, end='')

        except Exception as e:
            print("Exception: " + str(e))

rulesbroken(linetoexecute)