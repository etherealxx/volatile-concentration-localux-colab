import os, subprocess, sys, shlex, pickle, re

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

everyextension = pickleload(None, 'fullextensions')

additionalextension = [
    'a1111-sd-webui-tagcomplete', 'stable-diffusion-webui-composable-lora'
]  #@Ahmedkel's and @basedholychad's request

templist = [x for x in everyextension if x not in additionalextension]
pickledump(templist, 'tempext')