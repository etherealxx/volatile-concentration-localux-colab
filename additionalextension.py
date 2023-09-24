import os, pickle

vclvarpath = '/content/vlc'
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
    return exts

# Dumped from the main colab notebook. List of extension names
everyextension = pickleload(None, 'fullextensions')

additionalextensions = list_additional_ext()

extnameonly = [x.split("/")[-1] for x in additionalextensions] # Separating extension (repo) name from the full github link

# Extensions that are from camenduru's repo
templist = [x for x in everyextension if x not in extnameonly]
pickledump(templist, 'tempext')
