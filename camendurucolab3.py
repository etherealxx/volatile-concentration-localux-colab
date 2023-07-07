import os, subprocess, shlex, pickle, re, shutil

debugmode = False
curdir = '/'
linetoexecute_part1, linetoexecute_part2, linetoexecute_part2_1, linetoexecute_part2_2, linetoexecute_part3 = [], [], [], [], []
startcapture = False
afteraria = False
currentpart = 'part1'
parttoexecute = 'part1'
currentbranch = 'stable'
emptymodel = False

filename = 'stable_diffusion_1_5_webui_colab.ipynb'

vclvarpath = '/content/vclvariables'

def pickleload(prevvalue, inputfile):
  inputpath = os.path.join(vclvarpath, inputfile + '.pkl')
  if os.path.exists(inputpath):
      with open(inputpath, 'rb') as f:
          vartopass = pickle.load(f)
          return vartopass
  else:
    return prevvalue

# def printdebug(toprint):
#     if debugmode:
#         print(toprint)

colaboptions = pickleload(None, 'colaboptions')
if colaboptions:
  currentbranch = colaboptions["branch"]
  parttoexecute = colaboptions["part"]
  filename = colaboptions["filename"]
  emptymodel = colaboptions["empty_model"]


colabpath = f"/content/camendurus/{currentbranch}/{filename}"

if debugmode==True:
    colabpath = r"C:\Users\Ethereal\Downloads\526_mix_webui_colab.ipynb"

print("[1;32mGathering code from " + colabpath + "...")
print('[0m')

camendururepo = 'camenduru/stable-diffusion-webui'

with open(colabpath, 'r', encoding='utf-8') as f:
    for line in f:
        stripped_line = line.strip()
        if stripped_line.startswith(r'"%cd /content'):
            startcapture = True
        if startcapture:
            if stripped_line.startswith('"'):
                stripped_line = stripped_line[1:]
            if stripped_line.startswith('!'):
                stripped_line = stripped_line[1:]
            if stripped_line.endswith('\\n",'):
                stripped_line = stripped_line[:-4]
            if stripped_line.startswith(r'%env LD'):
                currentpart = 'part2'
                # print("[1;33mprepare " + currentpart + "[0m: " + stripped_line)
            elif stripped_line.startswith("git clone") and "https://github.com" in stripped_line and not stripped_line.endswith(camendururepo):
                currentpart = 'part2_1'
                # print("[1;33mprepare " + currentpart + "[0m: " + stripped_line)
            elif stripped_line.startswith("%cd /content/stable-diffusion-webui"):
                currentpart = "part2_2"
                # print("[1;33mprepare " + currentpart + "[0m: " + stripped_line)
            elif stripped_line.startswith('sed'):
                currentpart = 'part3'
                # print("[1;33mprepare " + currentpart + "[0m: " + stripped_line)
            
            #camendururepo = 'camenduru/stable-diffusion-webui'
            if camendururepo in stripped_line and not '/content/volatile-concentration-localux' in stripped_line:
                if camendururepo in stripped_line and (stripped_line.find(camendururepo) + len(camendururepo) == len(stripped_line) or stripped_line[stripped_line.find(camendururepo) + len(camendururepo)] in [' ', '\n']):
                    stripped_line += ' /content/volatile-concentration-localux'
            if currentbranch == "lite":
                if "https://download.pytorch.org/whl/cu116" in stripped_line and not "torchmetrics==0.11.4" in stripped_line:
                    line_parts = stripped_line.partition("--extra-index-url")
                    stripped_line = line_parts[0].strip() + " torchmetrics==0.11.4 " + line_parts[1] + line_parts[2]
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
                    elif currentpart == 'part2_1':
                        linetoexecute_part2_1.append(commandtoappend)
                    elif currentpart == 'part2_2':
                        linetoexecute_part2_2.append(commandtoappend)
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
            else:
                try:
                    if curdir:
                        print("[1;32m" + line)
                        print('[0m')
                        splittedcommand = shlex.split(line)
                        process = subprocess.Popen(splittedcommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd=curdir)
                        while True:
                            nextline = process.stdout.readline()
                            if nextline == '' and process.poll() is not None:
                                break
                            else:
                                if "%" in nextline.strip():
                                    stripnext = nextline.strip()
                                    print("\r", end="")
                                    print(f"\r{stripnext}", end='')
                                else:
                                    print(nextline, end='')

                except Exception as e:
                    print("Exception: " + str(e))

extensionlines = pickleload(linetoexecute_part2_1, 'extensions')
extensiontoremove = pickleload(None, 'removedextensions')
installextensions = []

for ext_line in extensionlines:
    pattern = r"https://github.com/\S+/(\S+)"
    match = re.search(pattern, ext_line)
    if match:
        ext_name = match.group(1)
        if not ext_name in extensiontoremove:
            installextensions.append(ext_line)

if debugmode==True:
    debugline(linetoexecute_part1)
else:
    if parttoexecute == 'part1':
        # print("[1;33m" + parttoexecute + "[0m")
        rulesbroken(linetoexecute_part1)
    elif parttoexecute == 'part2':
        # print("[1;33m" + "part2" + "[0m")
        rulesbroken(linetoexecute_part2)
        # rulesbroken(linetoexecute_part2_1)
        # print("[1;33m" + "part2_1" + "[0m")
        rulesbroken(installextensions)
        # print("[1;33m" + "part2_2" + "[0m")
        rulesbroken(linetoexecute_part2_2)
    elif parttoexecute == 'part3':
        # print("[1;33m" + parttoexecute + "[0m")
        rulesbroken(linetoexecute_part3)

for removed_ext in extensiontoremove:
    pattern = r"https://github.com/\S+/(\S+)"
    match = re.search(pattern, ext_line)
    if match:
        ext_name = match.group(1)
        if not ext_name in extensiontoremove:
            installextensions.append(ext_line)

if extensiontoremove and not emptymodel:
  for ext in extensiontoremove:
    extpath = os.path.join('/content/volatile-concentration-localux/extensions', ext)
    if os.path.exists(extpath):
      shutil.rmtree(extpath)
      print(f"removed {ext} extension")