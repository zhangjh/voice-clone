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
## 模型整合
cd ${work_dir}/GPT_SoVITS/pretrained_models
cat s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.part.* > s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2
tar -jxvf s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2 && rm s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2
tar -jxvf s2D488k.pth.bz2

cd chinese-hubert-base/
cat pytorch_model.bin.bz2.part.* > pytorch_model.bin.bz2
tar -jxvf pytorch_model.bin.bz2 && rm pytorch_model.bin.bz2

cd ../chinese-roberta-wwm-ext-large
cat pytorch_model.bin.bz2.part.* > pytorch_model.bin.bz2
tar -jxvf pytorch_model.bin.bz2 && rm pytorch_model.bin.bz2

python3 ${work_dir}/api.py -dr "${sample_audio}" -dt "${sample_text}" -dl "${lang}" -cp "${split}"
