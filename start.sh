#!/bin/bash
#### author: zhangjihong
#### desc: 启动ai服务

lang="zh"
split="，。？！,.?!"
work_dir=`pwd`

cp .condarc ~/
bash -c "
        conda init
        conda create -n GPTSoVits python=3.9 -y
        source activate GPTSoVits
        pip install -r requirements.txt
        ## 模型整合
        cd ${work_dir}/GPT_SoVITS/pretrained_models
        cat s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2.part.* | bunzip2 | tar x
        tar -jxvf s2G488k.pth.bz2

        cd chinese-hubert-base/
        cat pytorch_model.bin.bz2.part.* | bunzip2 | tar x

        cd ../chinese-roberta-wwm-ext-large
        cat pytorch_model.bin.bz2.part.* | bunzip2 | tar x

        cd ${work_dir}


        python3 ${work_dir}/api.py -dl "${lang}" -cp "${split}"
"