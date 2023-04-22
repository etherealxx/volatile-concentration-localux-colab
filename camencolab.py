import os, subprocess, sys, shlex

debugmode = False
curdir = '/'
linetoexecute_part1, linetoexecute_part2, linetoexecute_part3 = [], [], []
startcapture = False
afteraria = False
currentpart = 'part1'
parttoexecute = 'part1'
currentbranch = 'stable'
partargs, branchargs, filenameargs = '', '', ''
filename = 'stable_diffusion_1_5_webui_colab.ipynb'

if len(sys.argv) == 2:
    filenameargs = sys.argv[1]
    filename = filenameargs

if len(sys.argv) == 3:
    branchargs = sys.argv[2]
    currentbranch = branchargs

if len(sys.argv) == 4:
    partargs = sys.argv[3]
    parttoexecute = partargs

colabpath = f"/content/camendurus/{currentbranch}/{filename}"
if debugmode==True:
    colabpath = r"C:\Users\Ethereal\Downloads\526_mix_webui_colab.ipynb"

with open(colabpath, 'r', encoding='utf-8') as f:
    for line in f:
        stripped_line = line.strip()
        if stripped_line.startswith(r'"%cd /content'):
            startcapture = True
        # if stripped_line.startswith(r'"%env'):
        #     startcapture = True
        # if stripped_line == r'"%cd /content/stable-diffusion-webui\n",':
        #     startcapture = False
        if startcapture:
            if stripped_line.startswith('"'):
                stripped_line = stripped_line[1:]
            if stripped_line.startswith('!'):
                stripped_line = stripped_line[1:]
            if stripped_line.endswith('\\n",'):
                stripped_line = stripped_line[:-4]
            if stripped_line.startswith(r'%env LD'):
                currentpart = 'part2'
            elif stripped_line.startswith('sed'):
                currentpart = 'part3'
            if stripped_line:
                if stripped_line.startswith('aria2c') and not '4x-UltraSharp.pth' in stripped_line:
                    pass
                elif stripped_line.startswith(r'%env'):
                    pass
                elif stripped_line.startswith('python launch.py'):
                    pass
                elif stripped_line=='rm *.deb':
                    pass
                else:
                    commandtoappend = stripped_line.replace('/content/stable-diffusion-webui', '/content/volatile-concentration-localux')
                    if currentpart == 'part1':
                        linetoexecute_part1.append(commandtoappend)
                    elif currentpart == 'part2':
                        linetoexecute_part2.append(commandtoappend)
                    elif currentpart == 'part3':
                        linetoexecute_part3.append(commandtoappend)
            if stripped_line.startswith('python launch.py'):
                startcapture = False

def debugline(codetodebug):
    if codetodebug:
        # print(linetoexecute)
        for line in codetodebug:
            print(line)

def rulesbroken(codetoexecute, cwd=''):
    global curdir
    for line in codetoexecute:
        line = line.strip()
        if line.startswith('!'):
            line = line[1:]
        if not line == '':
            if line.startswith(r'%cd'):
                curdir = line.replace(r'%cd', '').strip()
            elif 'reset --hard' in line:
                if 'stable-diffusion-stability-ai' in line:
                    subprocess.run(["git", "reset", "--hard"], cwd="/content/volatile-concentration-localux/repositories/stable-diffusion-stability-ai")
                else:
                    subprocess.run(["git", "reset", "--hard"], cwd="/content/volatile-concentration-localux")
            else:
                try:
                    if curdir:
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
if debugmode==True:
    debugline(linetoexecute_part1)
else:
    if parttoexecute == 'part1':
        rulesbroken(linetoexecute_part1)
    elif parttoexecute == 'part2':
        rulesbroken(linetoexecute_part2)
    elif parttoexecute == 'part3':
        rulesbroken(linetoexecute_part3)