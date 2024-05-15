#!/bin/bash
#### author: zhangjihong
#### desc: 启动ai服务

sample_audio="$1"
sample_text="$2"
lang="zh"
split="，。？！,.?!"
work_dir=`pwd`
#conda create -n GPTSoVits python=3.9
#conda activate GPTSoVits
python3 ${work_dir}/api.py -dr "${sample_audio}" -dt "${sample_text}" -dl "${lang}" -cp "${split}"
