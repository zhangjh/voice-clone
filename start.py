import os
import subprocess
import shutil

def concatenate_and_extract(file_pattern, output_file):
    with open(output_file, 'wb') as outfile:
        for part in glob.glob(file_pattern):
            with open(part, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
    subprocess.run(['tar', '-jxvf', output_file], check=True)
    os.remove(output_file)

def main(sample_audio, sample_text):
    lang = "zh"
    split = "，。？！,.?!"
    work_dir = os.getcwd()

    # Model integration steps
    models_dir = os.path.join(work_dir, "GPT_SoVITS", "pretrained_models")
    os.chdir(models_dir)
    
    concatenate_and_extract('s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.part.*', 's1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2')
    subprocess.run(['tar', '-jxvf', 's2D488k.pth.bz2'], check=True)

    os.chdir(os.path.join(models_dir, "chinese-hubert-base"))
    concatenate_and_extract('pytorch_model.bin.bz2.part.*', 'pytorch_model.bin.bz2')
    subprocess.run(['tar', '-jxvf', 'pytorch_model.bin.bz2'], check=True)
    os.remove('pytorch_model.bin.bz2')

    os.chdir(os.path.join(models_dir, "../chinese-roberta-wwm-ext-large"))
    concatenate_and_extract('pytorch_model.bin.bz2.part.*', 'pytorch_model.bin.bz2')
    subprocess.run(['tar', '-jxvf', 'pytorch_model.bin.bz2'], check=True)
    os.remove('pytorch_model.bin.bz2')

    # Running the API script
    api_script_path = os.path.join(work_dir, "api.py")
    subprocess.run(['python3', api_script_path, '-dr', sample_audio, '-dt', sample_text, '-dl', lang, '-cp', split], check=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <sample_audio> <sample_text>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

