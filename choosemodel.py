import os, math, subprocess, pickle

# subprocess.run("apt -y install -qq aria2", shell=True, check=True)

everycolab = '/content/camendurus/lite'
everycolabname = []
colabnamepair = []
for colabname in os.listdir(everycolab):
  colabnamepruned = colabname.partition('_webui_colab.ipynb')[0]
  everycolabname.append(colabnamepruned)

sortedcolabname = sorted(everycolabname)
totalcolabcount = len(everycolabname)
for i, colabname in enumerate(sortedcolabname):
  halfall = math.ceil(totalcolabcount / 2)
  numberedname = "{} | {}".format(i, colabname.ljust(30))
  if i <= halfall:
    colabnamepair.append(numberedname)
  else:
    rev_index = (i - halfall) - 1
    colabnamepair[rev_index] += "\t" + numberedname

for colabpair in colabnamepair:
  print(colabpair)

choosenumber = input('Choose the number of the model you want: ')
if choosenumber.isdigit() and int(choosenumber) < totalcolabcount:
  chosencolabname = sortedcolabname[int(choosenumber)] + '_webui_colab.ipynb'
  print("Model from " + chosencolabname + " will be downloaded immediately after all the dependencies is installed. Please wait")

aria2c_lines = []
with open(os.path.join(everycolab, chosencolabname), 'r', encoding='utf-8') as f:
    for line in f:
        stripped_line = line.strip()
        if stripped_line.startswith('"!aria2c'):
            aria2c_lines.append(stripped_line)

with open('/content/arialist.pkl', 'wb') as f:
    pickle.dump(aria2c_lines, f)