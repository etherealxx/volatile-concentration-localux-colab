import os, pickle

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
    return exts
    
everyextension = pickleload(None, 'fullextensions')

additionalextensions = list_additional_ext()

extnameonly = [x.split("/")[-1] for x in additionalextensions]
templist = [x for x in everyextension if x not in extnameonly]
pickledump(templist, 'tempext')