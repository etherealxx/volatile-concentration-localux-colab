import os, subprocess, sys

partargs = sys.argv[1]
curdir = '/'
testpath = r"C:\Users\Ethereal\Downloads\526_mix_webui_colab.ipynb"
linetoexecute_part1, linetoexecute_part2, linetoexecute_part3 = [], [], []
startcapture = False
afteraria = False
currentpart = 'part1'
parttoexecute = 'part1'
if partargs:
    parttoexecute = partargs

with open(testpath, 'r', encoding='utf-8') as f:
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

debugline(linetoexecute_part1)

def rulesbroken(codetoexecute, cwd=''):
    for line in codetoexecute:
        line = line.strip()
        if line.startswith('!'):
            line = line[1:]
        if not line == '':
            if line.startswith(r'%cd'):
                curdir = line.replace(r'%cd', '').strip()
            else:
                try:
                    if curdir:
                        subprocess.run(line, shell=True, check=True, cwd=curdir)
                    else:
                        subprocess.run(line, shell=True, check=True)
                except Exception as e:
                    print("Exception: " + str(e))

if parttoexecute == 'part1':
    rulesbroken(linetoexecute_part1)
elif parttoexecute == 'part2':
    rulesbroken(linetoexecute_part1)
elif parttoexecute == 'part3':
    rulesbroken(linetoexecute_part1)