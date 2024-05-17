import os
import subprocess
import shutil

def run_command(command):
    """Run a shell command and handle errors."""
    print(os.getcwd())
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {command}")

def main():
    lang = "zh"
    split = "，。？！,.?!"
    work_dir = os.getcwd()

    # Copy .condarc to home directory
    shutil.copy('.condarc', os.path.expanduser('~'))

    run_command("bash setup_conda.sh")

    # Model integration
    pretrained_models_dir = os.path.join(work_dir, 'GPT_SoVITS', 'pretrained_models')
    os.chdir(pretrained_models_dir)

    # Combine and extract s1bert model files
    run_command("cat s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2.part.* | bunzip2 | tar x")

    # Extract s2G488k model file
    run_command("tar -jxvf s2G488k.pth.bz2")

    # Combine and extract chinese-hubert-base model files
    chinese_hubert_base_dir = os.path.join(pretrained_models_dir, 'chinese-hubert-base')
    os.chdir(chinese_hubert_base_dir)
    run_command("cat pytorch_model.bin.bz2.part.* | bunzip2 | tar x")

    # Combine and extract chinese-roberta-wwm-ext-large model files
    chinese_roberta_wwm_ext_large_dir = os.path.join(pretrained_models_dir, 'chinese-roberta-wwm-ext-large')
    os.chdir(chinese_roberta_wwm_ext_large_dir)
    run_command("cat pytorch_model.bin.bz2.part.* | bunzip2 | tar x")

    # Change back to work directory
    os.chdir(work_dir)

    # Run the Python API script
    run_command(f"python3 {os.path.join(work_dir, 'api.py')} -dl \"{lang}\" -cp \"{split}\"")

if __name__ == "__main__":
    main()
