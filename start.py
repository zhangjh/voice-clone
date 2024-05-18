import os
import subprocess
import shutil

def run_command(command):
    """Run a shell command and check for errors."""
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

def main():
    lang = "zh"
    split = "，。？！,.?!"
    work_dir = os.getcwd()

    # Copy .condarc to home directory
    shutil.copy('.condarc', os.path.expanduser('~'))

    # Execute commands in a bash shell
    bash_commands = f"""
    conda init
    conda create -n GPTSoVits python=3.9 -y
    source activate GPTSoVits
    pip install -r requirements.txt

    # Model integration
    cd {work_dir}/GPT_SoVITS/pretrained_models
    cat s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt.bz2.part.* | bunzip2 | tar x
    tar -jxvf s2G488k.pth.bz2

    cd chinese-hubert-base/
    cat pytorch_model.bin.bz2.part.* | bunzip2 | tar x

    cd ../chinese-roberta-wwm-ext-large
    cat pytorch_model.bin.bz2.part.* | bunzip2 | tar x

    cd {work_dir}

    # Run the Python script
    python3 {work_dir}/api.py -dl "{lang}" -cp "{split}"
    """

    # Run the bash commands
    run_command(f'bash -c "{bash_commands}"')

if __name__ == "__main__":
    main()
