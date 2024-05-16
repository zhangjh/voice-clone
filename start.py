
import os
import subprocess
import sys

def concatenate_and_extract(file_pattern, output_file):
    with open(output_file, 'wb') as outfile:
        for part in glob.glob(file_pattern):
            with open(part, 'rb') as infile:
                outfile.write(infile.read())
    subprocess.run(['tar', '-jxvf', output_file], check=True)
    os.remove(output_file)

def main(sample_audio, sample_text):
    lang = "zh"
    split = "，。？！,.?!"
    work_dir = os.getcwd()

    # 模型整合
    models_dir = os.path.join(work_dir, 'GPT_SoVITS', 'pretrained_models')
    os.chdir(models_dir)
    concatenate_and_extract('s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2.part.*', 
                            's1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2')
    subprocess.run(['tar', '-jxvf', 's2G488k.pth.bz2'], check=True)

    os.chdir(os.path.join(models_dir, 'chinese-hubert-base'))
    concatenate_and_extract('pytorch_model.bin.bz2.part.*', 'pytorch_model.bin.bz2')
    subprocess.run(['tar', '-jxvf', 'pytorch_model.bin.bz2'], check=True)
    os.remove('pytorch_model.bin.bz2')

    os.chdir(os.path.join(models_dir, '../chinese-roberta-wwm-ext-large'))
    concatenate_and_extract('pytorch_model.bin.bz2.part.*', 'pytorch_model.bin.bz2')
    subprocess.run(['tar', '-jxvf', 'pytorch_model.bin.bz2'], check=True)
    os.remove('pytorch_model.bin.bz2')

    # 执行API
    api_script = os.path.join(work_dir, 'api.py')
    args = ['-dl', lang, '-cp', split]
    if sample_audio or sample_text:
        args.extend(['-dr', sample_audio, '-dt', sample_text])
    subprocess.run(['python3', api_script] + args, check=True)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "", 
         sys.argv[2] if len(sys.argv) > 2 else "")