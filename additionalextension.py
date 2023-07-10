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

additionalextensions = [
    "https://github.com/a2569875/stable-diffusion-webui-composable-lora", #@basedholychad's request
    "https://github.com/DominikDoom/a1111-sd-webui-tagcomplete", #@Ahmedkel's request
    "https://github.com/hnmr293/sd-webui-cutoff", #@Orbimac's request (and 3 other extensions below)
    "https://github.com/zanllp/sd-webui-infinite-image-browsing",
    "https://github.com/Coyote-A/ultimate-upscale-for-automatic1111",
    "https://github.com/Bing-su/adetailer"
] # You can make a pull request and add your desired extension link here

extnameonly = [x.split("/")[-1] for x in additionalextensions]
templist = [x for x in everyextension if x not in extnameonly]
pickledump(templist, 'tempext')