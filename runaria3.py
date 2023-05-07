import os, pickle, subprocess

arialines = None
downloadcnet = False

vclvarpath = '/content/vclvariables'
def pickleload(prevvalue, inputfile):
  inputpath = os.path.join(vclvarpath, inputfile + '.pkl')
  if os.path.exists(inputpath):
      with open(inputpath, 'rb') as f:
          vartopass = pickle.load(f)
          return vartopass
  else:
    return prevvalue

arialines = pickleload(None, 'arialist')
colaboptions = pickleload(None, 'colaboptions')
if colaboptions:
  downloadcnet = colaboptions["controlnet"]
  downloadmodels = colaboptions["download_model"]

def subprocessing(execline):
  try:
    print("[1;32m" + execline)
    print('[0m')
    subprocess.run(execline, shell=True, check=True)
  except Exception as e:
      print("Exception: " + str(e))

if arialines:
  for line in arialines:
    if not '4x-UltraSharp.pth' in line:
      ariaexecline = line[2:].replace('\\n",', '').replace('/content/stable-diffusion-webui', '/content/volatile-concentration-localux')
      if 'ControlNet' in ariaexecline:
         if downloadcnet:
            subprocessing(ariaexecline)
      else:
        if downloadmodels:
          subprocessing(ariaexecline)

