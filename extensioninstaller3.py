import os, pickle, re

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

def list_additional_ext():
  addext_txtpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "additionalextensions.txt")
  with open(addext_txtpath, 'r') as file:
    lines = [line.rstrip('\n') for line in file]
    exts = [ext for ext in lines if ext != "" and not ext.startswith("#")]
    commits = [ext.lstrip("#commit") for ext in lines if ext != "" and ext.startswith("#commit")]
    branches = [ext.lstrip("#branch") for ext in lines if ext != "" and ext.startswith("#branch")]
    return exts, commits, branches

additionalextensions, additionalcommits, additionalbranches = list_additional_ext()

# Dumped from the main colab
colaboptions = pickleload(None, 'colaboptions')
if colaboptions:
  currentbranch = colaboptions["branch"]
  filename = colaboptions["filename"]

colabpath = f"/content/camendurus/{currentbranch}/{filename}"
if debugmode==True:
    colabpath = r"C:\Users\Ethereal\Downloads\526_mix_webui_colab.ipynb"

extensionpath = "/content/volatile-concentration-localux/extensions/"

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
            if stripped_line.startswith("git clone") and "https://github.com" in stripped_line:
                commandtoappend = stripped_line.replace('/content/stable-diffusion-webui', '/content/volatile-concentration-localux')
                extensionlines.append(commandtoappend)

for addextgithublink in additionalextensions:
    gitclonestring = 'git clone https://github.com/'
    repoowner = addextgithublink.split("/")[-2]
    reponame = addextgithublink.split("/")[-1]
    for branchline in additionalbranches:
        if reponame in branchline:
            specificbranch = branchline.lstrip(reponame).strip()
            gitclonestring = f'git clone -b {specificbranch} https://github.com/'
            break

    extensionlines.append(f"{gitclonestring}{repoowner}/{reponame} {extensionpath}{reponame}")
    for commitline in additionalcommits:
        if reponame in commitline:
            specificcommit = commitline.lstrip(reponame).strip()
            extensionlines.append(f"git checkout {specificcommit} .")
            break

# extensionlines.append(f"{gitclonestring}a2569875/stable-diffusion-webui-composable-lora {extensionpath}stable-diffusion-webui-composable-lora")
# extensionlines.append(f"{gitclonestring}DominikDoom/a1111-sd-webui-tagcomplete {extensionpath}a1111-sd-webui-tagcomplete")

# List of git clone lines (and now also git checkout, though won't work as espected currently)
pickledump(extensionlines, 'extensions')