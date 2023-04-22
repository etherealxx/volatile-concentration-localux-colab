import os, pickle, subprocess

arialines = None

if os.path.exists('/content/arialist.pkl'):
  with open('/content/arialist.pkl', 'rb') as f:
      arialines = pickle.load(f)

if arialines:
  for line in arialines:
    if not '4x-UltraSharp.pth' in line:
      ariaexecline = line[2:].replace('\\n",', '').replace('/content/stable-diffusion-webui', '/content/volatile-concentration-localux')
      try:
        print("[1;32m" + ariaexecline)
        print('[0m')
        subprocess.run(ariaexecline, shell=True, check=True)
      except Exception as e:
          print("Exception: " + str(e))