import subprocess
import os

def init():
    #删除candidate-img和capture-img文件夹下的所有文件
    for filename in os.listdir(r"./chara/workspace/candidate-img"):
        file_path = os.path.join(r"./chara/workspace/candidate-img", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    for filename in os.listdir(r"./chara/workspace/capture-img"):
        file_path = os.path.join(r"./chara/workspace/capture-img", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def task():
    result1 = subprocess.run(['python', './chara/workspace/prepared-img.py'], capture_output=True, text=True)
    print("standard output:", result1.stdout)
    print("error output:", result1.stderr)
    print("return code:", result1.returncode)
    result2 = subprocess.run(['python','./chara/workspace/pre-prepare.py'], capture_output=True, text=True)
    print("standard output:", result2.stdout)
    print("error output:", result2.stderr)
    print("return code:", result2.returncode)

if __name__ == "__main__":
    init()
    task()