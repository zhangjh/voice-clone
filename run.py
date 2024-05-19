
if __name__ == "__main__":
    # 打印当前路径
    print(f"当前路径: {os.getcwd()}")
    bash_commands = f"""
        source activate GPTSoVits
        cd /home/voice-clone
        python3 api.py -dl "zh" -cp "，。？！,.?!"
    """

