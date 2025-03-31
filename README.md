[![SVG Banners](https://svg-banners.vercel.app/api?type=rainbow&text1=FunClip%20%20🥒&width=800&height=210)](https://github.com/Akshay090/svg-banners)

### <p align="center">「[简体中文](./README_zh.md) | English」</p>

**<p align="center"> ⚡ Open-source, accurate and easy-to-use video clipping tool </p>**
**<p align="center"> 🧠 Explore LLM based video clipping with FunClip </p>**

<p align="center"> <img src="docs/images/interface.jpg" width=444/></p>

<p align="center" class="trendshift">
<a href="https://trendshift.io/repositories/10126" target="_blank"><img src="https://trendshift.io/api/badge/repositories/10126" alt="alibaba-damo-academy%2FFunClip | Trendshift" style="width: 250px; height: 55px;" width="300" height="55"/></a>
</p>

<div align="center">  
<h4>
<a href="#What's New"> What's New </a>
｜<a href="#On Going"> On Going </a>
｜<a href="#Install"> Install </a>
｜<a href="#Usage"> Usage </a>
｜<a href="#Community"> Community </ a>
</h4>
</div>

**FunClip** is a fully open-source, locally deployed automated video clipping tool. It leverages Alibaba TONGYI speech lab's open-source [FunASR](https://github.com/alibaba-damo-academy/FunASR) Paraformer series models to perform speech recognition on videos. Then, users can freely choose text segments or speakers from the recognition results and click the clip button to obtain the video clip corresponding to the selected segments (Quick Experience [Modelscope⭐](https://modelscope.cn/studios/iic/funasr_app_clipvideo/summary) [HuggingFace🤗](https://huggingface.co/spaces/R1ckShi/FunClip)).

## Highlights🎨

- 🔥Try AI clipping using LLM in FunClip now.
- FunClip integrates Alibaba's open-source industrial-grade model [Paraformer-Large](https://modelscope.cn/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/summary), which is one of the best-performing open-source Chinese ASR models available, with over 13 million downloads on Modelscope. It can also accurately predict timestamps in an integrated manner.
- FunClip incorporates the hotword customization feature of [SeACo-Paraformer](https://modelscope.cn/models/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/summary), allowing users to specify certain entity words, names, etc., as hotwords during the ASR process to enhance recognition results.
- FunClip integrates the [CAM++](https://modelscope.cn/models/iic/speech_campplus_sv_zh-cn_16k-common/summary) speaker recognition model, enabling users to use the auto-recognized speaker ID as the target for trimming, to clip segments from a specific speaker.
- The functionalities are realized through Gradio interaction, offering simple installation and ease of use. It can also be deployed on a server and accessed via a browser.
- FunClip supports multi-segment free clipping and automatically returns full video SRT subtitles and target segment SRT subtitles, offering a simple and convenient user experience.

<a name="What's New"></a>
## What's New🚀
- 2024/06/12 FunClip supports recognize and clip English audio files now. Run `python funclip/launch.py -l en` to try.
- 🔥2024/05/13 FunClip v2.0.0 now supports smart clipping with large language models, integrating models from the qwen series, GPT series, etc., providing default prompts. You can also explore and share tips for setting prompts, the usage is as follows:
  1. After the recognition, select the name of the large model and configure your own apikey;
  2. Click on the 'LLM Inference' button, and FunClip will automatically combine two prompts with the video's srt subtitles;
  3. Click on the 'AI Clip' button, and based on the output results of the large language model from the previous step, FunClip will extract the timestamps for clipping;
  4. You can try changing the prompt to leverage the capabilities of the large language models to get the results you want;
- 2024/05/09 FunClip updated to v1.1.0, including the following updates and fixes:
  - Support configuration of output file directory, saving ASR intermediate results and video clipping intermediate files;
  - UI upgrade (see guide picture below), video and audio cropping function are on the same page now, button position adjustment;
  - Fixed a bug introduced due to FunASR interface upgrade, which has caused some serious clipping errors;
  - Support configuring different start and end time offsets for each paragraph;
  - Code update, etc;
- 2024/03/06 Fix bugs in using FunClip with command line.
- 2024/02/28 [FunASR](https://github.com/alibaba-damo-academy/FunASR) is updated to 1.0 version, use FunASR1.0 and SeACo-Paraformer to conduct ASR with hotword customization.
- 2023/10/17 Fix bugs in multiple periods chosen, used to return video with wrong length.
- 2023/10/10 FunClipper now supports recognizing with speaker diarization ability, choose 'yes' button in 'Recognize Speakers' and you will get recognition results with speaker id for each sentence. And then you can clip out the periods of one or some speakers (e.g. 'spk0' or 'spk0#spk3') using FunClipper.

<a name="On Going"></a>
## On Going🌵

- [x] FunClip will support Whisper model for English users, coming soon (ASR using Whisper with timestamp requires massive GPU memory, we support timestamp prediction for vanilla Paraformer in FunASR to achieving this).
- [x] FunClip will further explore the abilities of large langage model based AI clipping, welcome to discuss about prompt setting and clipping, etc.
- [ ] Reverse periods choosing while clipping.
- [ ] Removing silence periods.

<a name="Install"></a>
## Install🔨

### Python env install

FunClip basic functions rely on a python environment only.
```shell
# clone funclip repo
git clone https://github.com/alibaba-damo-academy/FunClip.git
cd FunClip
# install Python requirments
pip install -r ./requirements.txt
```

### imagemagick install (Optional)

If you want to clip video file with embedded subtitles

1. ffmpeg and imagemagick is required

- On Ubuntu
```shell
apt-get -y update && apt-get -y install ffmpeg imagemagick
sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml
```
- On MacOS
```shell
brew install imagemagick
sed -i 's/none/read,write/g]