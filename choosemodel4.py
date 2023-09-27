import os, math, subprocess, pickle, sys

branchtype = 'lite'

if len(sys.argv) == 2:
    branchargs = sys.argv[1]
    branchtype = branchargs

import gradio as gr

# subprocess.run("apt -y install -qq aria2", shell=True, check=True)

everycolab = f'/usr/kame/{branchtype}'
everycolabname = []
colabnamepair = []
for colabname in os.listdir(everycolab):
  colabnamepruned = colabname.partition('_webui_colab.ipynb')[0]
  everycolabname.append(colabnamepruned)

sortedcolabname = sorted(everycolabname)

vclvarpath = '/usr/vlc'
def pickledump(vartodump, outputfile):
  outputpath = os.path.join(vclvarpath, outputfile + '.pkl')
  with open(outputpath, 'wb') as f:
      pickle.dump(vartodump, f)

# 'sortedcolabname' will be accessed by the main colab notebook
pickledump(sortedcolabname, 'sortedcolabname')


# totalcolabcount = len(everycolabname)
# for i, colabname in enumerate(sortedcolabname):
#   halfall = math.ceil(totalcolabcount / 2)
#   numberedname = "{} | {}".format(i, colabname.ljust(30))
#   if i <= halfall:
#     colabnamepair.append(numberedname)
#   else:
#     rev_index = (i - halfall) - 1
#     colabnamepair[rev_index] += "\t" + numberedname

# for colabpair in colabnamepair:
#   print(colabpair)

# chosencolabname = ''

# while True:
#   choosenumber = input('Choose the number of the model you want: ')
#   if choosenumber.isdigit() and int(choosenumber) < totalcolabcount:
#     chosencolabname = sortedcolabname[int(choosenumber)] + '_webui_colab.ipynb'
#     print("Model from " + chosencolabname + " will be downloaded immediately after all the dependencies is installed. Please wait")
#     break
#   elif choosenumber == '':
#     print("No model will be pre-downloaded. Dependencies installation will continue.")
#     break

# aria2c_lines = []

# if chosencolabname:
#    if os.path.exists(os.path.join(everycolab, chosencolabname)):
#       with open(os.path.join(everycolab, chosencolabname), 'r', encoding='utf-8') as f:
#           for line in f:
#               stripped_line = line.strip()
#               if stripped_line.startswith('"!aria2c'):
#                   aria2c_lines.append(stripped_line)

# if aria2c_lines:
#   with open('/usr/arialist.pkl', 'wb') as f:
#       pickle.dump(aria2c_lines, f)
