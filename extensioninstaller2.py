import os, subprocess, sys, shlex, pickle, re

debugmode = False
curdir = '/'
startcapture = False
afteraria = False
currentbranch = 'stable'
extensionlines = []

filename = 'stable_diffusion_1_5_webui_colab.ipynb'

vclvarpath = '/content/vclvariables'
def pickledump(vartodump, outputfile):
  outputpath = os.path.join(vclvarpath, outputfile + '.pkl')
  with open(outputpath, 'wb') as f:
      pickle.dump(vartodump, f)

def pickleload(prevvalue, inputfile):
  inputpath = os.path.join(vclvarpath, inputfile + '.pkl')
  if os.path.exists(inputpath):
      with open(inputpath, 'rb') as f:
          vartopass = pickle.load(f)
          return vartopass
  else:
    return prevvalue

colaboptions = pickleload(None, 'colaboptions')
if colaboptions:
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

pickledump(extensionlines, 'extensions')