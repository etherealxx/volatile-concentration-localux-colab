import os, subprocess, sys, shlex, pickle, re

debugmode = False
curdir = '/'
startcapture = False
afteraria = False
currentbranch = 'stable'
colaboptions = None
extensionlines = []

filename = 'stable_diffusion_1_5_webui_colab.ipynb'

if os.path.exists('/content/colaboptions.pkl'):
  with open('/content/colaboptions.pkl', 'rb') as f:
      colaboptions = pickle.load(f)
      currentbranch = colaboptions["branch"]
      filename = colaboptions["filename"]

colabpath = f"/content/camendurus/{currentbranch}/{filename}"
if debugmode==True:
    colabpath = r"C:\Users\Ethereal\Downloads\526_mix_webui_colab.ipynb"

with open(colabpath, 'r', encoding='utf-8') as f:
    pattern = r"(?<!\S)https://github.com/camenduru/stable-diffusion-webui(?!\S)"
    for line in f:
        stripped_line = line.strip()
        if stripped_line.startswith('"'):
            stripped_line = stripped_line[1:]
        if stripped_line.startswith('!'):
            stripped_line = stripped_line[1:]
        if stripped_line.endswith('\\n",'):
            stripped_line = stripped_line[:-4]
        if not startcapture:
            if re.search(pattern, stripped_line):
                startcapture = True
        else:
            camendururepo = 'camenduru/stable-diffusion-webui'
            if camendururepo in stripped_line and not '/content/volatile-concentration-localux' in stripped_line:
                if camendururepo in stripped_line and (stripped_line.find(camendururepo) + len(camendururepo) == len(stripped_line) or stripped_line[stripped_line.find(camendururepo) + len(camendururepo)] in [' ', '\n']):
                    stripped_line += ' /content/volatile-concentration-localux'
            if stripped_line.startswith('git clone https://github.com/'):
                commandtoappend = stripped_line.replace('/content/stable-diffusion-webui', '/content/volatile-concentration-localux')
                extensionlines.append(commandtoappend)

with open('/content/extensions.pkl', 'wb') as f:
    pickle.dump(extensionlines, f)

# def debugline(codetodebug):
#     if codetodebug:
#         # print(linetoexecute)
#         for line in codetodebug:
#             print(line)

# def rulesbroken(codetoexecute, cwd=''):
#     global curdir
#     for line in codetoexecute:
#         line = line.strip()
#         if line.startswith('!'):
#             line = line[1:]
#         if not line == '':
#             if line.startswith(r'%cd'):
#                 curdir = line.replace(r'%cd', '').strip()
#             else:
#                 try:
#                     if curdir:
#                         print("[1;32m" + line)
#                         print('[0m')
#                         splittedcommand = shlex.split(line)
#                         # subprocess.run(line, shell=True, check=True, cwd=curdir)
#                         process = subprocess.Popen(splittedcommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd=curdir)
#                         while True:
#                             # Read the output from the process
#                             nextline = process.stdout.readline()
#                             if nextline == '' and process.poll() is not None:
#                                 break
#                             # Check if the line contains progress information
#                             else:
#                                 if "%" in nextline.strip():
#                                     stripnext = nextline.strip()
#                                     print("\r", end="")
#                                     print(f"\r{stripnext}", end='')
#                                 else:
#                                     print(nextline, end='')

#                 except Exception as e:
#                     print("Exception: " + str(e))