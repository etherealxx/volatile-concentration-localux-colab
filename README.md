[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/etherealxx/volatile-concentration-localux-colab/blob/main/volatile_concentration_localux_colab.ipynb) <- Click here to access the colab
# Project VCL-Colab
Another camenduru colab ~~clone~~ alternative.😋

Features:
- All camenduru colab flavor in one single colab
- Bypass the damned google colab warning (when it detects `stable-diffusion-webui` and `sd-webui` string)
- Option to choose model from a Gradio UI directly on Colab cell output
- Automatic update, synced in real time with Camenduru's repo

The automatic update works by basically scraping from camenduru's repo, so it will automatically update the model list everytime camenduru's repo got new models.<br/>
As long as he doesn't change much on the repo code, this colab will always works without the need to maintain it.

Basically proof-of-concept. Would like to hear feedbacks and suggestion on the issues page.

Huge thanks to [camenduru](https://github.com/camenduru), without him this colab wouldn't be possible. Check out his [original repo](https://github.com/camenduru/stable-diffusion-webui-colab).

### ⚠️ Things to Note!
- The usual `/content/stable-diffusion-webui` is renamed to `/content/volatile-concentration-localux`, just keep in mind. Every file and folder inside is normal. (Pretty obvious though)

### ⚠️ Got an Error 403?
Read [here](https://github.com/etherealxx/volatile-concentration-localux-colab/blob/main/error403guide.md) for guide to fix it.

### 🆙 Latest Update:
- 22/07/2023 (July): Added a little bit of documentation on the colab notebook. Removed unused old scripts. Fixed bug where unticking `choose_model` while at the same time ticking `controlnet_models` on the notebook makes SD fails to launch. Now changing branch after running the main cell atleast once will preserve the previously downloaded models and generated outputs.
- 20/07/2023 (July): Added functionality for the extension installer where extension's branch and commits are choosable in `additionalextensions.txt`. Removed the whole `libtcmalloc` lines. Adjusted the way this colab gather the code with the recent changes.
- 10/07/2023 (July): Added `sd-webui-cutoff`, `sd-webui-infinite-image-browsing`, `ultimate-upscale-for-automatic1111`, and `adetailer` as optional choosable extension. Now optional extensions are stored on `additionalextensions.txt`. Now optional extensions are listed at the bottom of the extension checkboxes on the gradio UI.
- 07/07/2023 (July): Fixed some typo in the repo extract code (fixed lite branch). Added `torchmetrics==0.11.4` as an additional dependency for lite branch.
- 02/07/2023 (July): Bypass the new colab warning that detects `sd-webui` string.
- 16/06/2023 (June): Added `a1111-sd-webui-tagcomplete` and `composable-lora extension` as optional choosable extension. Fixed 'all extension is missing' bug.
