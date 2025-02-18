#!/bin/bash
#### author: zhangjihong
#### desc: ai环境依赖
#### 前置依赖：已经安装好了显卡驱动、conda

conda install -c conda-forge gcc
conda install -c conda-forge gxx
conda install -c ffmpeg cmake
conda install pytorch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt